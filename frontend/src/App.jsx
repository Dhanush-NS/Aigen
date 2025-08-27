import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function useAuth() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const save = (t) => { setToken(t); localStorage.setItem("token", t); };
  const clear = () => { setToken(""); localStorage.removeItem("token"); };
  return { token, save, clear };
}

// ---------------- Login ----------------
function Login({ onAuthed }) {
  const [email, setEmail] = useState("");
  const [password, setPw] = useState("");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    const form = new URLSearchParams();
    form.append("username", email); // backend uses email as "username"
    form.append("password", password);
    try {
      const r = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form.toString()
      });
      if (!r.ok) throw new Error("Login failed");
      const data = await r.json();
      onAuthed(data.access_token);
    } catch (err) { setError(err.message); }
  };

  return (
    <div className="card max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-3">Login</h2>
      <form onSubmit={submit} className="space-y-3">
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} className="w-full"/>
        <input placeholder="Password" type="password" value={password} onChange={e=>setPw(e.target.value)} className="w-full"/>
        <button className="w-full bg-black text-white">Login</button>
      </form>
      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}

// ---------------- Register ----------------
function Register() {
  const [username, setU] = useState("");
  const [email, setE] = useState("");
  const [password, setP] = useState("");
  const [ok, setOk] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    const r = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ username, email, password })
    });
    setOk(r.ok ? "Registered! Now login." : "Failed (maybe already exists).");
  };

  return (
    <div className="card max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-3">Register</h2>
      <form onSubmit={submit} className="space-y-3">
        <input placeholder="Username" value={username} onChange={e=>setU(e.target.value)} className="w-full"/>
        <input placeholder="Email" value={email} onChange={e=>setE(e.target.value)} className="w-full"/>
        <input placeholder="Password" type="password" value={password} onChange={e=>setP(e.target.value)} className="w-full"/>
        <button className="w-full bg-black text-white">Register</button>
      </form>
      {ok && <p className="mt-2">{ok}</p>}
    </div>
  );
}

// ---------------- Search ----------------
function Search({ token, onSaved }) {
  const [q, setQ] = useState("");
  const [results, setRes] = useState([]);

  const go = async () => {
    const r = await fetch(`${API_URL}/search?q=${encodeURIComponent(q)}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await r.json();
    setRes(data.results || []);
    onSaved(); // refresh dashboard
  };

  return (
    <div className="card">
      <h3 className="font-semibold mb-2">Web Search</h3>
      <div className="flex gap-2">
        <input className="flex-1" placeholder="Search…" value={q} onChange={e=>setQ(e.target.value)}/>
        <button onClick={go} className="bg-black text-white">Search</button>
      </div>
      <ul className="mt-3 space-y-2">
        {results.map((r,i)=>(
          <li key={i} className="border p-2 rounded">
            <a href={r.href} target="_blank" rel="noreferrer" className="font-medium">{r.title}</a>
            <p className="text-sm">{r.body}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

// ---------------- Image Generation ----------------
function ImageGen({ token, onSaved }) {
  const [prompt, setPrompt] = useState("");
  const [img, setImg] = useState("");

  const gen = async () => {
    const r = await fetch(`${API_URL}/image`, {
      method: "POST",
      headers: {
        "Content-Type":"application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ prompt })
    });
    const data = await r.json();
    setImg(data.image_url);
    onSaved();
  };

  return (
    <div className="card">
      <h3 className="font-semibold mb-2">Image Generation</h3>
      <div className="flex gap-2">
        <input className="flex-1" placeholder="e.g., astronaut riding a unicorn" value={prompt} onChange={e=>setPrompt(e.target.value)}/>
        <button onClick={gen} className="bg-black text-white">Generate</button>
      </div>
      {img && <img src={img} alt="result" className="mt-3 rounded"/>}
    </div>
  );
}

// ---------------- Dashboard ----------------
function Dashboard({ token, reloadFlag }) {
  const [items, setItems] = useState([]);

  const load = async () => {
    const r = await fetch(`${API_URL}/dashboard`, { headers: { Authorization: `Bearer ${token}` }});
    const data = await r.json();
    setItems(data.items || []);
  };
  useEffect(()=>{ load(); }, [reloadFlag]);

  const del = async (id) => {
    await fetch(`${API_URL}/dashboard/${id}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` }});
    load();
  };

  return (
    <div className="card">
      <h3 className="font-semibold mb-3">Dashboard</h3>
      <ul className="space-y-2">
        {items.map(it=>(
          <li key={it.id} className="border p-2 rounded">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs px-2 py-1 bg-gray-100 rounded mr-2">{it.item_type}</span>
                <span className="font-medium">{it.query}</span>
              </div>
              <button onClick={()=>del(it.id)} className="text-sm">Delete</button>
            </div>
            {it.item_type === "image" && it.data?.image_url && (
              <img src={it.data.image_url} alt="" className="mt-2 rounded max-h-48" />
            )}
            {it.item_type === "search" && Array.isArray(it.data?.results) && (
              <ul className="mt-2 list-disc ml-6">
                {it.data.results.slice(0,3).map((r,i)=>(
                  <li key={i}><a className="underline" href={r.href} target="_blank" rel="noreferrer">{r.title}</a></li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

// ---------------- App ----------------
export default function App() {
  const auth = useAuth();
  const [reload, setReload] = useState(0);
  const onSaved = () => setReload((n)=>n+1);

  // If not logged in
  if (!auth.token) {
    return (
      <div className="max-w-5xl mx-auto p-4 space-y-6">
        <h1 className="text-3xl font-bold">AI-Gen</h1>
        <div className="grid md:grid-cols-2 gap-6">
          <Login onAuthed={auth.save}/>
          <Register/>
        </div>
      </div>
    );
  }

  // If logged in
  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">AI-Gen</h1>
        <button onClick={auth.clear} className="bg-gray-200 px-3 py-1 rounded">Logout</button>
      </header>
      <div className="grid md:grid-cols-2 gap-6">
        <Search token={auth.token} onSaved={onSaved}/>
        <ImageGen token={auth.token} onSaved={onSaved}/>
      </div>
      <Dashboard token={auth.token} reloadFlag={reload}/>
    </div>
  );
}
