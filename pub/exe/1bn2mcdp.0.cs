﻿using System;using src.pub.network;namespace nettest{class Program{static public void accept(string client_token){Console.WriteLine(client_token);}static public string receive(string client_token, string data){Console.WriteLine(client_token+":"+data);return null;}static void Main(string[] args){network.TCP_Server_Start(accept,receive,7097);network.Keep_Alive();}}}