import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket, threading, json, datetime, hashlib

HOST   = "127.0.0.1"
PORT   = 55560
ROOMS  = ["General", "Tech", "Random", "Games"]
COLORS = ["#58A6FF","#3FB950","#FF7B72","#D29922","#BC8CFF","#FF9E64"]
EMOJIS = ["😀","😂","😍","🔥","👍","❤️","😎","🎉","😢","🤔","👋","✅","🚀","💬","🎊","🌟"]

BG   = "#0D1117"
CARD = "#161B22"
INP  = "#21262D"
BDR  = "#30363D"
TW   = "#E6EDF3"
TG   = "#8B949E"
GRN  = "#3FB950"
BLU  = "#58A6FF"
RED  = "#F85149"

# ═══════════════════════════════════════════════════════════
#  SERVER
# ═══════════════════════════════════════════════════════════
_clients = {}
_rooms   = {r: [] for r in ROOMS}
_history = {r: [] for r in ROOMS}
_users   = {}
_cidx    = 0

def _hash(p):  return hashlib.sha256(p.encode()).hexdigest()
def _now():    return datetime.datetime.now().strftime("%I:%M %p")

def _send(sock, data):
    try:   sock.send((json.dumps(data) + "\n").encode())
    except: pass

def _broom(room, data, skip=None):
    for s in _rooms.get(room, []):
        if s != skip: _send(s, data)

def _ball(data, skip=None):
    for s in _clients:
        if s != skip: _send(s, data)

def _online(): return [v["u"] for v in _clients.values()]

def _srv_handle(sock):
    buf = ""
    try:
        while True:
            chunk = sock.recv(4096).decode()
            if not chunk: break
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                if line.strip():
                    try: _srv_process(sock, json.loads(line))
                    except: pass
    except: pass
    finally: _srv_drop(sock)

def _srv_process(sock, d):
    global _cidx
    a = d.get("action")

    if a == "register":
        u, p = d["u"].strip(), d["p"]
        if u in _users:
            _send(sock, {"a": "fail", "msg": "Username already taken!"})
        else:
            _users[u] = _hash(p)
            _send(sock, {"a": "ok_reg"})

    elif a == "login":
        u, p = d["u"].strip(), d["p"]
        if u in _users and _users[u] == _hash(p):
            col = COLORS[_cidx % len(COLORS)]; _cidx += 1
            _clients[sock] = {"u": u, "room": "General", "col": col}
            _rooms["General"].append(sock)
            _send(sock, {
                "a": "ok_login", "u": u, "col": col,
                "room": "General", "rooms": ROOMS,
                "hist": _history["General"][-30:]
            })
            _broom("General", {"a":"sys","msg":f"👋 {u} joined #General","t":_now()}, skip=sock)
            _ball({"a": "who", "users": _online()})
        else:
            _send(sock, {"a": "fail", "msg": "Wrong username or password!"})

    elif a == "msg":
        if sock not in _clients: return
        info = _clients[sock]
        room, u, col = info["room"], info["u"], info["col"]
        txt = d.get("txt", "").strip()
        if not txt: return
        m = {"a":"msg","u":u,"col":col,"txt":txt,"t":_now(),"room":room}
        _history[room].append(m)
        if len(_history[room]) > 100: _history[room] = _history[room][-100:]
        _broom(room, m)

    elif a == "switch":
        if sock not in _clients: return
        info = _clients[sock]
        old, new, u = info["room"], d.get("room"), info["u"]
        if new not in ROOMS: return
        if sock in _rooms[old]: _rooms[old].remove(sock)
        _broom(old, {"a":"sys","msg":f"👋 {u} left #{old}","t":_now()})
        _rooms[new].append(sock)
        _clients[sock]["room"] = new
        _send(sock, {"a":"switched","room":new,"hist":_history[new][-30:]})
        _broom(new, {"a":"sys","msg":f"👋 {u} joined #{new}","t":_now()}, skip=sock)

def _srv_drop(sock):
    if sock in _clients:
        info = _clients[sock]; u, room = info["u"], info["room"]
        if sock in _rooms.get(room, []): _rooms[room].remove(sock)
        _broom(room, {"a":"sys","msg":f"❌ {u} left the chat","t":_now()})
        del _clients[sock]
        _ball({"a": "who", "users": _online()})
    try: sock.close()
    except: pass

def _run_server(log_fn):
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT)); srv.listen()
    log_fn(f"✅ Server ready on {HOST}:{PORT}")
    log_fn("📢 Waiting for users to connect...")
    while True:
        try:
            srv.settimeout(1)
            try:
                s, addr = srv.accept()
                log_fn(f"🔗 New connection: {addr[0]}:{addr[1]}")
                threading.Thread(target=_srv_handle, args=(s,), daemon=True).start()
            except socket.timeout: continue
        except: break

# ═══════════════════════════════════════════════════════════
#  SERVER WINDOW
# ═══════════════════════════════════════════════════════════
class ServerWindow:
    def __init__(self, root):
        self.root = root
        root.title("💬 Chat Server")
        root.geometry("500x400")
        root.configure(bg=BG)

        tk.Label(root, text="💬 Chat Server Running",
            font=("Helvetica",16,"bold"), bg=BG, fg=TW).pack(pady=16)
        tk.Label(root,
            text="Open another terminal → run again → Join Chat",
            font=("Helvetica",10), bg=BG, fg=TG).pack()
        tk.Frame(root, bg=BDR, height=1).pack(fill="x", padx=24, pady=12)
        tk.Label(root, text="Server Logs:",
            font=("Helvetica",10), bg=BG, fg=TG).pack(anchor="w", padx=24)

        self.logs = scrolledtext.ScrolledText(root,
            font=("Courier New",10), bg=INP, fg=GRN,
            relief="flat", bd=8, state="disabled")
        self.logs.pack(fill="both", expand=True, padx=24, pady=(4,24))

        threading.Thread(target=_run_server, args=(self._log,), daemon=True).start()

    def _log(self, msg):
        self.root.after(0, self.__log, msg)

    def __log(self, msg):
        self.logs.config(state="normal")
        self.logs.insert(tk.END, f"[{_now()}] {msg}\n")
        self.logs.config(state="disabled")
        self.logs.see(tk.END)

# ═══════════════════════════════════════════════════════════
#  LOGIN WINDOW
# ═══════════════════════════════════════════════════════════
class LoginWindow:
    def __init__(self, root, on_done):
        self.root = root
        self.on_done = on_done
        self.mode = tk.StringVar(value="login")

        tk.Label(root, text="💬 Chat App",
            font=("Georgia",22,"bold"), bg=BG, fg=TW).pack(pady=(36,4))
        tk.Label(root, text="Rooms • Emojis • Login • History",
            font=("Helvetica",10), bg=BG, fg=TG).pack()
        tk.Frame(root, bg=BDR, height=1).pack(fill="x", padx=24, pady=20)

        mf = tk.Frame(root, bg=BG); mf.pack()
        for txt, val in [("Login","login"),("Register","register")]:
            tk.Radiobutton(mf, text=txt, variable=self.mode, value=val,
                bg=BG, fg=TW, selectcolor=INP,
                activebackground=BG, font=("Helvetica",11,"bold")
            ).pack(side="left", padx=20)

        for label, attr, show in [("Username","_ue",""),("Password","_pe","●")]:
            tk.Label(root, text=label, font=("Helvetica",10),
                bg=BG, fg=TG).pack(anchor="w", padx=40, pady=(14,2))
            e = tk.Entry(root, font=("Helvetica",12),
                bg=INP, fg=TW, insertbackground=TW,
                relief="flat", bd=10, show=show)
            e.pack(fill="x", padx=40)
            setattr(self, attr, e)

        self._pe.bind("<Return>", lambda e: self._go())

        self._err = tk.Label(root, text="",
            font=("Helvetica",10), bg=BG, fg=RED)
        self._err.pack(pady=(10,0))

        tk.Button(root, text="Continue →",
            font=("Helvetica",11,"bold"), bg=GRN, fg="#000",
            relief="flat", bd=0, padx=24, pady=11,
            cursor="hand2", command=self._go).pack(pady=18)

    def _go(self):
        u = self._ue.get().strip()
        p = self._pe.get().strip()
        if not u or not p:
            self._err.config(text="Please fill in both fields!"); return
        self._err.config(text="Connecting...")
        self.root.after(100, lambda: self.on_done(u, p, self.mode.get()))

# ═══════════════════════════════════════════════════════════
#  CHAT WINDOW
# ═══════════════════════════════════════════════════════════
class ChatWindow:
    def __init__(self, root, sock, u, col, room, rooms, hist):
        self.root = root
        self.sock = sock
        self.u    = u
        self.col  = col
        self.room = room
        self.buf  = ""

        root.title(f"💬 {u} — #{room}")
        root.geometry("860x620")
        root.configure(bg=BG)
        root.protocol("WM_DELETE_WINDOW", self._close)
        self._build()
        self._load(hist)
        threading.Thread(target=self._recv, daemon=True).start()

    def _build(self):
        # ── Left sidebar ───────────────────────────────────
        sb = tk.Frame(self.root, bg=CARD, width=190)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="💬 Chat App",
            font=("Helvetica",13,"bold"), bg=CARD, fg=TW
        ).pack(pady=(16,2), padx=14, anchor="w")

        tk.Label(sb, text=f"👤 {self.u}",
            font=("Helvetica",10), bg=CARD, fg=self.col
        ).pack(padx=14, anchor="w")

        tk.Frame(sb, bg=BDR, height=1).pack(fill="x", padx=14, pady=10)

        tk.Label(sb, text="ROOMS",
            font=("Helvetica",9,"bold"), bg=CARD, fg=TG
        ).pack(padx=14, anchor="w")

        self._rbts = {}
        for r in ROOMS:
            b = tk.Button(sb, text=f"# {r}",
                font=("Helvetica",10), bg=CARD, fg=TG,
                relief="flat", bd=0, padx=14, pady=7,
                cursor="hand2", anchor="w",
                command=lambda rm=r: self._switch(rm))
            b.pack(fill="x")
            self._rbts[r] = b
        self._hiroom(self.room)

        tk.Frame(sb, bg=BDR, height=1).pack(fill="x", padx=14, pady=10)
        tk.Label(sb, text="ONLINE",
            font=("Helvetica",9,"bold"), bg=CARD, fg=TG
        ).pack(padx=14, anchor="w")
        self._onf = tk.Frame(sb, bg=CARD)
        self._onf.pack(fill="x", padx=8)

        # ── Right main area ────────────────────────────────
        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Header
        hdr = tk.Frame(main, bg=CARD, padx=16, pady=10)
        hdr.pack(side="top", fill="x")
        self._rlbl = tk.Label(hdr, text=f"# {self.room}",
            font=("Helvetica",14,"bold"), bg=CARD, fg=TW)
        self._rlbl.pack(side="left")

        # ── IMPORTANT: pack bottom widgets FIRST ──────────
        # Input row at very bottom
        ir = tk.Frame(main, bg=INP, padx=10, pady=10)
        ir.pack(side="bottom", fill="x", padx=10, pady=(0,10))

        self._entry = tk.Entry(ir,
            font=("Helvetica",13), bg=INP, fg=TW,
            insertbackground=TW, relief="flat", bd=6)
        self._entry.pack(side="left", fill="x", expand=True, ipady=8)
        self._entry.bind("<Return>", lambda e: self._send())
        self._entry.focus_set()

        tk.Button(ir, text="  Send ➤  ",
            font=("Helvetica",11,"bold"), bg=BLU, fg="#000",
            relief="flat", bd=0, padx=10, pady=8,
            cursor="hand2", command=self._send
        ).pack(side="left", padx=(10,0))

        # Emoji bar above input
        ef = tk.Frame(main, bg=CARD, pady=5)
        ef.pack(side="bottom", fill="x", padx=10)
        for em in EMOJIS:
            tk.Button(ef, text=em,
                font=("Helvetica",14), bg=CARD, fg=TW,
                relief="flat", bd=0, padx=4,
                cursor="hand2",
                command=lambda e=em: self._emoji(e)
            ).pack(side="left")

        # Chat area fills all remaining space
        self._chat = scrolledtext.ScrolledText(main,
            font=("Helvetica",11), bg=BG, fg=TW,
            relief="flat", bd=0, state="disabled",
            wrap="word", spacing3=6)
        self._chat.pack(side="top", fill="both",
                        expand=True, padx=10, pady=(8,0))

        # Text tags
        self._chat.tag_config("sys",
            foreground=TG, font=("Helvetica",10,"italic"))
        self._chat.tag_config("ts",
            foreground=TG, font=("Helvetica",9))
        self._chat.tag_config("me",
            foreground="#AFFFBF", background="#1A3A2A")

    def _hiroom(self, room):
        for r, b in self._rbts.items():
            if r == room:
                b.config(bg=INP, fg=TW, font=("Helvetica",10,"bold"))
            else:
                b.config(bg=CARD, fg=TG, font=("Helvetica",10))

    def _emoji(self, e):
        self._entry.insert(tk.END, e)
        self._entry.focus_set()

    def _put_msg(self, u, txt, t, col, me=False):
        self._chat.config(state="normal")
        if me:
            self._chat.insert(tk.END, f"\n  [{t}]  You: {txt}\n", "me")
        else:
            self._chat.insert(tk.END, f"\n  [{t}]  ", "ts")
            tag = f"u_{u}"
            self._chat.insert(tk.END, f"{u}: ", tag)
            self._chat.tag_config(tag, foreground=col,
                font=("Helvetica",11,"bold"))
            self._chat.insert(tk.END, f"{txt}\n")
        self._chat.config(state="disabled")
        self._chat.see(tk.END)

    def _put_sys(self, msg, t=""):
        self._chat.config(state="normal")
        line = f"\n  ── {msg}" + (f"  [{t}]" if t else "") + " ──\n"
        self._chat.insert(tk.END, line, "sys")
        self._chat.config(state="disabled")
        self._chat.see(tk.END)

    def _load(self, hist):
        if not hist:
            self._put_sys(f"Welcome to #{self.room}! Start chatting 👋")
            return
        self._put_sys("── Previous Messages ──")
        for m in hist:
            self._put_msg(m["u"], m["txt"], m["t"], m["col"],
                          me=(m["u"] == self.u))

    def _send(self):
        txt = self._entry.get().strip()
        if not txt: return
        self._entry.delete(0, tk.END)
        try:
            self.sock.send((json.dumps({"action":"msg","txt":txt})+"\n").encode())
        except:
            messagebox.showerror("Error","Connection lost!")
            return
        self._put_msg(self.u, txt, _now(), self.col, me=True)

    def _switch(self, room):
        if room == self.room: return
        try:
            self.sock.send(
                (json.dumps({"action":"switch","room":room})+"\n").encode())
        except: pass

    def _recv(self):
        while True:
            try:
                chunk = self.sock.recv(4096).decode()
                if not chunk: break
                self.buf += chunk
                while "\n" in self.buf:
                    line, self.buf = self.buf.split("\n", 1)
                    if line.strip():
                        try:
                            self.root.after(0, self._handle,
                                            json.loads(line))
                        except: pass
            except: break

    def _handle(self, d):
        a = d.get("a")
        if a == "msg":
            if d["u"] != self.u:
                self._put_msg(d["u"], d["txt"], d["t"], d["col"])
        elif a == "sys":
            self._put_sys(d["msg"], d.get("t",""))
        elif a == "switched":
            self.room = d["room"]
            self._rlbl.config(text=f"# {self.room}")
            self.root.title(f"💬 {self.u} — #{self.room}")
            self._hiroom(self.room)
            self._chat.config(state="normal")
            self._chat.delete("1.0", tk.END)
            self._chat.config(state="disabled")
            self._load(d.get("hist", []))
        elif a == "who":
            self._update_online(d["users"])

    def _update_online(self, users):
        for w in self._onf.winfo_children(): w.destroy()
        for u in users:
            tk.Label(self._onf, text=f"● {u}",
                font=("Helvetica",10), bg=CARD,
                fg=GRN if u == self.u else TG
            ).pack(anchor="w", padx=6, pady=2)

    def _close(self):
        try: self.sock.close()
        except: pass
        self.root.destroy()

# ═══════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════
class MenuWindow:
    def __init__(self, root):
        self.root = root
        root.title("💬 Advanced Chat App")
        root.geometry("400x340")
        root.configure(bg=BG)
        root.resizable(False, False)
        self._build()

    def _build(self):
        tk.Label(self.root, text="💬 Advanced Chat App",
            font=("Georgia",20,"bold"), bg=BG, fg=TW
        ).pack(pady=(40,4))
        tk.Label(self.root, text="Rooms  •  Emojis  •  Login  •  History",
            font=("Helvetica",10), bg=BG, fg=TG
        ).pack()
        tk.Frame(self.root, bg=BDR, height=1).pack(
            fill="x", padx=40, pady=24)

        tk.Button(self.root, text="🖥️   Start Server",
            font=("Helvetica",13,"bold"), bg=GRN, fg="#000",
            relief="flat", bd=0, padx=20, pady=13,
            cursor="hand2", command=self._start_server
        ).pack(fill="x", padx=40)
        tk.Label(self.root, text="▲ Run this first in Terminal 1",
            font=("Helvetica",9), bg=BG, fg=TG
        ).pack(pady=(4,14))

        tk.Button(self.root, text="💬   Join Chat",
            font=("Helvetica",13,"bold"), bg=BLU, fg="#000",
            relief="flat", bd=0, padx=20, pady=13,
            cursor="hand2", command=self._join
        ).pack(fill="x", padx=40)
        tk.Label(self.root, text="▲ Run in Terminal 2 & 3 to chat",
            font=("Helvetica",9), bg=BG, fg=TG
        ).pack(pady=(4,0))

    def _clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def _start_server(self):
        self._clear()
        self.root.geometry("500x400")
        ServerWindow(self.root)

    def _join(self):
        self._clear()
        self.root.geometry("400x480")
        LoginWindow(self.root, self._auth)

    def _auth(self, u, p, mode):
        try:
            sock = socket.socket()
            sock.connect((HOST, PORT))
        except:
            messagebox.showerror("Connection Error",
                "❌ Cannot connect to server!\n\n"
                "Please start the server first:\n"
                "Open Terminal 1 → run → Start Server")
            self._join()
            return

        # Send register or login
        sock.send((json.dumps({"action":mode,"u":u,"p":p})+"\n").encode())

        # Wait for response
        buf = ""
        sock.settimeout(5)
        try:
            while True:
                buf += sock.recv(4096).decode()
                if "\n" in buf:
                    line, _ = buf.split("\n", 1)
                    r = json.loads(line)
                    break
        except:
            messagebox.showerror("Error","Server not responding!")
            sock.close()
            return
        sock.settimeout(None)

        # If registered → auto login now
        if r.get("a") == "ok_reg":
            sock.send((json.dumps({"action":"login","u":u,"p":p})+"\n").encode())
            buf = ""
            sock.settimeout(5)
            try:
                while True:
                    buf += sock.recv(4096).decode()
                    if "\n" in buf:
                        line, _ = buf.split("\n", 1)
                        r = json.loads(line)
                        break
            except:
                messagebox.showerror("Error","Login failed after register!")
                sock.close()
                return
            sock.settimeout(None)

        if r.get("a") == "fail":
            messagebox.showerror("Error", r["msg"])
            sock.close()
            self._join()
            return

        # Open chat!
        self._clear()
        ChatWindow(self.root, sock,
                   r["u"], r["col"],
                   r.get("room","General"),
                   r.get("rooms", ROOMS),
                   r.get("hist", []))

# ═══════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    MenuWindow(root)
    root.mainloop()