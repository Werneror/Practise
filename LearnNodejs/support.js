setTimeout(function(){
    console.log("进程 " + process.argv[2] + " 执行。" );
}, process.argv[2]*1000);
