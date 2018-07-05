function BackupTime() {
    # 备份当前时间
    Get-Date -Format 'yyyy-MM-dd hh:mm:ss' > $env:TEMP/backup_time.tmp
}
function GetTimeFromFile() {
    # 从备份文件获取时间
    try{
        return get-content $env:TEMP/backup_time.tmp
    } catch {
        return ''
    }
}
function GetTimeFromNet() {
    # 从网络获取当前时间
    try{
        $net_time_url = 'http://api.k780.com:88/?app=life.time&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json'
        $net_time_ret = Invoke-WebRequest -Uri $net_time_url -TimeoutSec 5
        $net_time_json = $net_time_ret.Content | ConvertFrom-Json
        return $net_time_json.result.datetime_1
    } catch {
        return ''    
    }
}
function Get-2012-Time() {
    $date = Get-Date
    return "2012-{0}-{1} {2}:{3}:{4}" -f $date.Month, $date.Day, $date.Hour, $date.Minute, $date.Second 
}
function Main() {
    $date = Get-Date
    $year = $date.Year
    if ($year -eq "2012") {
        $time = GetTimeFromNet
        if($time -eq "") {
            $time = GetTimeFromFile
        }
        Set-Date $time
    } else {
        BackupTime
        $time = Get-2012-Time
        Set-Date $time
    }
}
Main