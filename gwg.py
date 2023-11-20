import sys , socket , threading , getopt , subprocess
listher = False
command = True
exec = ""
host = ""
upload = ""
port = ""
def help():
    print('da')
def main():
    global listher , command , exec , upload , host
    try:
        opts , argvs = getopt.getopt(sys.argv[1:],"hle:a:p:cu" , ['help' , 'listen' , 'execute' ,'address','port' , 'command','upload'])
    except getopt.GetoptError as er :
        print(er)
    for o ,a in opts:
        if o in ("-h","--help"):
            help()
        elif o in ("-l","--listen"):
            listher = True
        elif o in ("-e","--execute"):
            exec = a
        elif o in ("-c","--command"):
            command = True
        elif o in ("-U","--upload"):
            upload = a
        elif o in ("-a","--address"):
            host = a
        elif o in ("-p","--port"):
            port= int(a)
        else:
            assert False , "wrong Input"
    if not listher and len(host) and port >= 0:
        buffer = sys.stdin.read()
        ch(buffer)
    if listher:
        sever_lop()
def ch(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((host,port))
        if len(buffer):
            client.send(buffer.encode())
        while True:
            recv = 1
            response = ""
            while recv:
                data = client.recv(1024)
                recv = data
                response += data.decode()
                if recv <= 1024:
                    break
            print(response)
            buffer = input("ff ")
            buffer += '\n'
            client.send(buffer.encode())
    except Exception as er:
        print(er)
        client.close()
def server():
    global host
    if not len(host):
        host="0.0.0.0"
    serve = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serve.bind((host,port))
    serve.listen(5)
    while True:
        client_s, data2 = serve.accept()
        cT = threading.Thread(target=c_hander,args=(client_s,))
        cT.start()
def c_hander(client_s):
    global upload,exec,command
    if len(upload):
        upfile = ""
        while True:
            data = client_s.recv(1024)
            if not data:
                break
            else:
                upfile += data
        try:
            with open(upload,'wb') as file:
                file.write(upfile)
            client_s.send('writf aLF')
        except Exception as e :
            client_s.send('write f')
    if len(exec):
        out = run_command(exec)
        client_s.send(out)
    if command:
        while True:
            client_s.send('shel')
            cbuf = b""
            while b"\n" not in cbuf:
                cbuf+= client_s.recv(1024)
            respon = run_command(cbuf.decode())
            client_s.send(respon)
def run_command(command):
    command = command.rstrip()
    try:
        out = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
        return out
    except Exception as e :
        return str(e)
main()

