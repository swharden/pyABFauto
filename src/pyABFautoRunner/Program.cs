﻿if (args is null || args.Length != 1)
    throw new InvalidOperationException("one argument is required: path to python file");

string pyFilePath = Path.GetFullPath(args[0]);
Console.WriteLine(pyFilePath);
if (!File.Exists(pyFilePath))
    throw new FileNotFoundException(pyFilePath);

System.Diagnostics.Process process = new();
process.StartInfo.FileName = "cmd.exe";
process.StartInfo.Arguments = $"/C python \"{pyFilePath}\"";
process.StartInfo.UseShellExecute = false;
process.StartInfo.CreateNoWindow = false;
process.StartInfo.RedirectStandardOutput = false;

while (true)
{
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine($"{DateTime.Now} Restarting: {pyFilePath}");
    Console.ResetColor();

    process.Start();
    while (!process.HasExited)
        Thread.Sleep(1000);
}