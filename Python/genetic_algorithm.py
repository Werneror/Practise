#!/usr/bin/python
# ^_^ coding:utf8 ^_^

import copy
import random

class Gene:
    u'基因（染色体）类，置某遗传算子概率为0可禁用该遗传算子'

    gene = str()

    def __init__(self,
                 length,
                 one_point_crossor_p,
                 two_point_crossor_p,
                 random_bit_exchange_p,
                 exchange_quantity,
                 general_mutation_p,
                 inversion_mutation_p):
        self.length = length
        self.one_point_crossor_p = one_point_crossor_p
        self.two_point_crossor_p = two_point_crossor_p
        self.random_bit_exchange_p = random_bit_exchange_p
        self.exchange_quantity = exchange_quantity if exchange_quantity < length else length
        self.general_mutation_p = general_mutation_p
        self.inversion_mutation_p = inversion_mutation_p

    def set_gene(self, gene):
        u'设置基因字符串'
        self.gene = gene

    def get_gene(self):
        u'返回基因字符串'
        return self.gene

    def crossor(self, other_gene):
        u'将多种重组算子封装在一起'
        self.one_point_crossor(self, other_gene)
        self.two_point_crossor(self, other_gene)
        self.random_bit_exchange(self, other_gene)

    def mutation(self):
        u'将多种变异算子封装在一起'
        self.general_mutation()
        self.inversion_mutation()

    def one_point_crossor(self, other_gene):
        u'重组算子：单点交叉'
        if random.random() < self.one_point_crossor_p:
            start = random.randint(0, self.length)
            exchange_string = self.gene[start:]
            self.gene = self.gene[0:start] + other_gene.gene[start:]
            other_gene.gene = other_gene.gene[0:start] + exchange_string

    def two_point_crossor(self, other_gene):
        u'重组算子：两点交叉'
        if random.random() < self.two_point_crossor_p:
            start = random.randint(0, self.length)
            end = random.randint(start, self.length)
            exchange_string = self.gene[start:end]
            self.gene = self.gene[0:start] + other_gene.gene[start:end] + self.gene[end:]
            other_gene.gene = other_gene.gene[0:start] + exchange_string + other_gene.gene[end:]

    def random_bit_exchange(self, other_gene):
        u'重组算子：随机串交换'
        if self.exchange_quantity > 0 and random.random() < self.random_bit_exchange_p:
            exchange_locations = list()
            while(len(exchange_locations) < self.exchange_quantity):
                location = random.randint(0, self.length-1)
                if location not in exchange_locations:
                    exchange_locations.append(location)
                    exchange_bit = self.gene[location]
                    self.gene = self.gene[0:location] + other_gene.gene[location:location+1] + self.gene[location+1:]
                    other_gene.gene = other_gene.gene[0:location] + exchange_bit + other_gene.gene[location+1:]

    def general_mutation(self):
        u'变异算子：普通变异'
        if self.general_mutation_p > 0 :
            new_gene = str()
            for g in self.gene:
                if random.random() < self.general_mutation_p:
                    new_gene += '0' if g == '1' else '1'
                else:
                    new_gene += g
            self.gene = new_gene

    def inversion_mutation(self):
        u'变异算子：逆序变异'
        if random.random() < self.general_mutation_p:
            start = random.randint(0, self.length)
            end = random.randint(start, self.length)
            self.gene = self.gene[0:start] + self.gene[start:end][::-1] + self.gene[end:]

class Population():
    u'种群类'

    generation = 0
    survival = list()
    best_individuals = list()
    fitness_avg = 0
    fitness_best = 0
    fitness_avg_increase = 0

    def __init__(self,
                 gene_length, # 基因长度
                 individual_quantity, # 个体总数
                 max_generation=0, # 终止条件：最大世代数，为0则不限制世代数
                 max_fitness=0, # 终止条件：最大适应度，为0则不限制最大适应度
                 min_fitness_avg_increase=0, # 终止条件：最小平均适应度增长，为0则无限制
                 one_point_crossor_p=0,
                 two_point_crossor_p=0.1,
                 random_bit_exchange_p=0,
                 exchange_quantity=0,
                 general_mutation_p=0.1,
                 inversion_mutation_p=0.1):

        self.individual_quantity = individual_quantity
        self.max_generation = max_generation
        self.max_fitness = max_fitness
        self.min_fitness_avg_increase = min_fitness_avg_increase

        while len(self.survival) < self.individual_quantity:
            individual = Gene(gene_length,
                              one_point_crossor_p,
                              two_point_crossor_p,
                              random_bit_exchange_p,
                              exchange_quantity,
                              general_mutation_p,
                              inversion_mutation_p)
            individual.set_gene(self.random_str(gene_length))
            self.survival.append(individual)

    def fortune_wheel(self):
        u'幸运轮，用于随机地筛选更适应环境的基因'
        survival_next = list()
        # 先计算所有存活个体的适应度之和
        fitness_sum = float()
        fitness_list = list()
        for individual in self.survival:
            fitness_sum += self.fitness_function(individual.get_gene())
            fitness_list.append(fitness_sum)
        # 然后以个体的适应度占适应度之和的比例为概率决定个体是否存活
        while len(survival_next) < len(self.survival):
            probability = random.random() * fitness_sum
            for individual, fitness_step in zip(self.survival, fitness_list):
                if fitness_step >= probability:
                    survival_next.append(copy.deepcopy(individual))
                    break
        # 更新存活个体
        self.survival = survival_next

    def mating_and_recombined(self):
        u'配对并重组，采用随机配对'
        # 先随机配对。在配对时认为个体是雌性同体的
        #   若存活个体总数为奇数，则会有一个个体没有配偶，该个体会直接进入下一轮
        female_list = list()
        male_list = list()
        status = True
        while len(female_list) + len(male_list) < len(self.survival):
            index = random.randint(0, len(self.survival)-1)
            if index not in female_list and index not in male_list:
                if status:
                    male_list.append(index)
                else:
                    female_list.append(index)
        # 然后进行重组（交配）
        for female, male in zip(female_list, male_list):
            self.survival[female].crossor(self.survival[male])

    def mutation(self):
        u'变异'
        for individual in self.survival:
            individual.mutation()

    def prevent_premature_degeneration(self):
        u'检测并防止过早退化'
        if len(self.survival) > 0:
            is_degeneration = True
            gene = self.survival[0].get_gene()
            for individual in self.survival[1:]:
                if individual.get_gene() != gene:
                    is_degeneration = False
                    break
            if is_degeneration:
                for individual in self.survival[len(self.survival)/2:]:
                    new_gene = self.random_str(len(gene))
                    individual.set_gene(new_gene)

    def run(self):
        u'开始执行遗传算法'
        while True:
            #a = raw_input("")
            self.prevent_premature_degeneration()
            self.fortune_wheel()
            self.mating_and_recombined()
            self.mutation()
            self.statistics()
            self.print_info()
            self.generation += 1
            if self.max_generation != 0 and self.generation > self.max_generation:
                print('generation is {} larger than {}, terminating.'.format(self.generation, self.max_generation))
                break
            if self.max_fitness != 0 and self.fitness_best >= self.max_fitness:
                print('The maximum value of fitness is {} not less than {}, terminating.'.format(self.fitness_best, self.max_fitness))
                break
            if self.min_fitness_avg_increase != 0 and self.fitness_avg_increase < self.min_fitness_avg_increase:
                print('The increase in the fitness average is {} less than {}, terminating.'.format(self.fitness_avg_increase, self.min_fitness_avg_increase))
                break

    def statistics(self):
        u'对存活个体进行一些统计'
        fitness_sum = float()
        self.fitness_best = 0
        self.best_individuals = list()
        for individual in self.survival:
            fitness = self.fitness_function(individual.get_gene())
            fitness_sum += fitness
            if fitness > self.fitness_best:
                self.fitness_best = fitness;
                self.best_individuals = list()
                self.best_individuals.append(individual)
            elif fitness == self.fitness_best:
                self.best_individuals.append(individual)
        avg = fitness_sum / len(self.survival)
        self.fitness_avg_increase = avg - self.fitness_avg
        self.fitness_avg = avg

    def print_info(self):
        u'在每个世代结束时输出一些信息的函数，建议覆盖此方法以输出想要的信息'
        print(u'# ' + str(self.generation) + ' #'*40)
        print(u'# 适应度最大值：{}'.format(self.fitness_best))
        print(u'# 适应度平均值：{}'.format(self.fitness_avg))
        print(u'# 适应度平均值增长量：{}'.format(self.fitness_avg_increase))
        print(u'# 最佳个体（适应度最大）基因：')
        for individual in self.best_individuals:
            print(u'# {}'.format(individual.get_gene()))

    def random_str(self, length):
        u'生成指定长度随机0、1字符串'
        ret_str = ''
        for i in range(length):
            ret_str += '0' if random.randint(0, 1) == 0 else '1'
        return ret_str

    def fitness_function(self, gene):
        u'适应函数（也叫做存活函数、进化函数等），需先覆盖此方法'
        raise NotImplementedError('You have to cover the method fitness_function first')

if __name__ == '__main__':

    class SamplePopulation(Population):
        def fitness_function(self, gene):
            u'求函数 f(x) = -0.05*x^2+4*x+1000 在0～255上的最大值'
            x = int(gene, 2)
            return -0.05 * (x**2) + 4*x + 1000

    sample = SamplePopulation(8, 8, 50) # 限定世代数为50
    sample.run()
