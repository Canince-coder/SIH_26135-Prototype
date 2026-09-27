import { createContext, useContext, useEffect, useState } from "react";
import { login as apiLogin, getMe } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("sb_user");
    return raw ? JSON.parse(raw) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("sb_token");
    if (!token) {
      setLoading(false);
      return;
    }
    getMe()
      .then((me) => {
        setUser(me);
        localStorage.setItem("sb_user", JSON.stringify(me));
      })
      .catch(() => {
        localStorage.removeItem("sb_token");
        localStorage.removeItem("sb_user");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    try {
      const { access_token } = await apiLogin(email, password);

      localStorage.setItem("sb_token", access_token);

      const me = await getMe();

      localStorage.setItem("sb_user", JSON.stringify(me));
      setUser(me);

      return me;
    } catch (error) {
      localStorage.removeItem("sb_token");
      localStorage.removeItem("sb_user");
      setUser(null);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("sb_token");
    localStorage.removeItem("sb_user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
