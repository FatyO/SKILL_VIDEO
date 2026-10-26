using System.Diagnostics;

var startInfo = new ProcessStartInfo
{
    FileName = "wsl.exe",
    UseShellExecute = false,
};

startInfo.ArgumentList.Add("-d");
startInfo.ArgumentList.Add("Ubuntu");
startInfo.ArgumentList.Add("--");
startInfo.ArgumentList.Add("/home/fatima/.local/bin/heygen");
foreach (var argument in args)
{
    startInfo.ArgumentList.Add(argument);
}

using var process = Process.Start(startInfo);
if (process is null)
{
    Console.Error.WriteLine("No se pudo iniciar HeyGen mediante WSL.");
    return 1;
}

process.WaitForExit();
return process.ExitCode;
