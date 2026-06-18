import socket

def test_dusttrak_ip(ip_address, port=3600):
    # 建立一個 TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0) # 設定 3 秒超時，避免程式無限卡死
    
    try:
        print(f"嘗試透過 TCP 連線至 {ip_address}:{port} ...")
        # 建立連線
        s.connect((ip_address, port))
        print("✅ 連線成功！儀器 TCP 埠開啟。")
        
        # 準備發送 ASCII 測試指令 (通常需要 \r 或 \r\n 結尾)
        # 假設發送讀取機型的指令，實際指令請參考 TSI 通訊手冊
        test_command = "READ_MODEL\r\n" 
        print(f"發送指令: {test_command.strip()}")
        s.sendall(test_command.encode('ascii'))
        
        # 讀取儀器回傳的數據 (最多讀取 1024 bytes)
        response = s.recv(1024).decode('ascii').strip()
        
        if response:
            print(f"📥 收到儀器回傳數據: {response}")
        else:
            print("連線成功，但儀器沒有回傳任何文字 (可能指令不對或格式錯誤)。")
            
    except socket.timeout:
        print("❌ 連線超時：找不到該 IP，或是儀器網路模組未啟動。")
    except ConnectionRefusedError:
        print(f"❌ 連線被拒絕：IP 正確，但 Port {port} 沒有開放。可以試著掃描其他 Port。")
    except Exception as e:
        print(f"⚠️ 發生未知的網路錯誤: {e}")
    finally:
        s.close()
        print("通訊端點已關閉。")

# 請將這裡的 IP 換成你在儀器螢幕上看到的 USB IP
test_dusttrak_ip('169.254.236.57', port=3600)