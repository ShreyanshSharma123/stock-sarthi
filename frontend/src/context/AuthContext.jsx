import { createContext, useContext, useState, useEffect } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem("token");
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await api.get("/users/me");
      setUser(response.data);
    } catch (error) {
      localStorage.removeItem("token");
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const payload = new URLSearchParams();
      payload.append("username", email);
      payload.append("password", password);

      const response = await api.post("/users/login", payload, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
      const { access_token, user: userData } = response.data;

      localStorage.setItem("token", access_token);
      setUser(userData);

      return userData;
    } catch (error) {
      // Extract error message from backend response
      let errorMessage = "Login failed. Please try again.";
      if (error.code === "ECONNABORTED") {
        errorMessage =
          "Server timeout. Please check backend server and try again.";
      } else if (error.message === "Network Error") {
        errorMessage =
          "Cannot reach backend server. Please make sure backend is running on port 8000.";
      }
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data) {
        // Handle Pydantic validation errors
        const data = error.response.data;
        if (Array.isArray(data)) {
          errorMessage = data.map((e) => e.msg || String(e)).join(", ");
        } else if (typeof data === "string") {
          errorMessage = data;
        }
      }
      throw new Error(errorMessage);
    }
  };

  const register = async (userData) => {
    const response = await api.post("/users/register", userData);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
