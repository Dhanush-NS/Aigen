import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ---------------- Auth Hook ----------------
function useAuth() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const save = (t) => { setToken(t); localStorage.setItem("token", t); };
  const clear = () => { setToken(""); localStorage.removeItem("token"); };
  return { token, save, clear };
}

// ---------------- Theme Hook ----------------
function useTheme() {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggle = () => setTheme(theme === "dark" ? "light" : "dark");
  return { theme, toggle };
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
    form.append("username", email);
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
    <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-gray-900 dark:text-gray-100">
      <h2 className="text-xl font-semibold mb-3">Login</h2>
      <form onSubmit={submit} className="space-y-3">
        <input
          placeholder="Email"
          value={email}
          onChange={e=>setEmail(e.target.value)}
          className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={e=>setPw(e.target.value)}
          className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
        />
        <button className="w-full bg-black text-white dark:bg-white dark:text-black p-2 rounded">
          Login
        </button>
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
    <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-gray-900 dark:text-gray-100">
      <h2 className="text-xl font-semibold mb-3">Register</h2>
      <form onSubmit={submit} className="space-y-3">
        <input
          placeholder="Username"
          value={username}
          onChange={e=>setU(e.target.value)}
          className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
        />
        <input
          placeholder="Email"
          value={email}
          onChange={e=>setE(e.target.value)}
          className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={e=>setP(e.target.value)}
          className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
        />
        <button className="w-full bg-black text-white dark:bg-white dark:text-black p-2 rounded">
          Register
        </button>
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
    onSaved();
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow">
      <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Web Search</h3>
      <div className="flex gap-2">
        <input
          className="flex-1 p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
          placeholder="Search…"
          value={q}
          onChange={e=>setQ(e.target.value)}
        />
        <button onClick={go} className="px-3 py-2 bg-black text-white dark:bg-white dark:text-black rounded">
          Search
        </button>
      </div>
      <ul className="mt-3 space-y-2">
        {results.map((r,i)=>(
          <li key={i} className="border p-2 rounded bg-gray-50 dark:bg-gray-700">
            <a href={r.href} target="_blank" rel="noreferrer" className="font-medium text-blue-600 dark:text-blue-400">{r.title}</a>
            <p className="text-sm text-gray-600 dark:text-gray-300">{r.body}</p>
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
    <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow">
      <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Image Generation</h3>
      <div className="flex gap-2">
        <input
          className="flex-1 p-2 border rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-300"
          placeholder="e.g., astronaut riding a unicorn"
          value={prompt}
          onChange={e=>setPrompt(e.target.value)}
        />
        <button onClick={gen} className="px-3 py-2 bg-black text-white dark:bg-white dark:text-black rounded">
          Generate
        </button>
      </div>
      {img && <img src={img} alt="result" className="mt-3 rounded shadow"/>}
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

  const downloadImage = async (url, name="download.png") => {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    } catch (err) {
      console.error("Failed to download image:", err);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow">
      <h3 className="font-semibold mb-3 text-gray-900 dark:text-gray-100">Dashboard</h3>
      <ul className="space-y-2">
        {items.map(it=>(
          <li key={it.id} className="border p-3 rounded bg-gray-50 dark:bg-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs px-2 py-1 bg-gray-200 dark:bg-gray-600 rounded mr-2 text-gray-800 dark:text-gray-200">
                  {it.item_type}
                </span>
                <span className="font-medium text-gray-900 dark:text-gray-100">{it.query}</span>
              </div>
              <div className="flex gap-2">
                {it.item_type === "image" && it.data?.image_url && (
                  <>
                    <button
                      onClick={()=>downloadImage(it.data.image_url, `image-${it.id}.png`)}
                      className="text-sm bg-blue-500 text-white px-2 py-1 rounded"
                    >
                      Download
                    </button>
                    <a
                      href={it.data.image_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-sm bg-green-500 text-white px-2 py-1 rounded"
                    >
                      View
                    </a>
                  </>
                )}
                <button
                  onClick={()=>del(it.id)}
                  className="text-sm bg-red-500 text-white px-2 py-1 rounded"
                >
                  Delete
                </button>
              </div>
            </div>
            {it.item_type === "image" && it.data?.image_url && (
              <img src={it.data.image_url} alt="" className="mt-2 rounded max-h-48 shadow"/>
            )}
            {it.item_type === "search" && Array.isArray(it.data?.results) && (
              <ul className="mt-2 list-disc ml-6 text-gray-900 dark:text-gray-100">
                {it.data.results.slice(0,3).map((r,i)=>( 
                  <li key={i}>
                    <a className="underline text-blue-600 dark:text-blue-400" href={r.href} target="_blank" rel="noreferrer">
                      {r.title}
                    </a>
                  </li>
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
  const { theme, toggle } = useTheme();
  const onSaved = () => setReload((n)=>n+1);

  if (!auth.token) {
    return (
      <div className="max-w-5xl mx-auto p-4 space-y-6 bg-gray-100 dark:bg-gray-900 min-h-screen text-gray-900 dark:text-gray-100">
        <header className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">AI-Gen</h1>
          <button onClick={toggle} className="px-3 py-1 rounded bg-gray-300 dark:bg-gray-700">
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
        </header>
        <div className="grid md:grid-cols-2 gap-6">
          <Login onAuthed={auth.save}/>
          <Register/>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6 bg-gray-100 dark:bg-gray-900 min-h-screen text-gray-900 dark:text-gray-100">
      <header className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">AI-Gen</h1>
        <div className="flex gap-2">
          <button onClick={toggle} className="px-3 py-1 rounded bg-gray-300 dark:bg-gray-700">
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
          <button onClick={auth.clear} className="bg-gray-300 dark:bg-gray-700 px-3 py-1 rounded">Logout</button>
        </div>
      </header>

      <div className="grid md:grid-cols-2 gap-6">
        <Search token={auth.token} onSaved={onSaved}/>
        <ImageGen token={auth.token} onSaved={onSaved}/>
      </div>
      <Dashboard token={auth.token} reloadFlag={reload}/>
    </div>
  );
}
