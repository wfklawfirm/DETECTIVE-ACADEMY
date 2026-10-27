"use client";
import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from "react";
import { IconButton } from "./button";
import { XIcon } from "./icons";

interface T { id: number; text: string }
const Ctx = createContext<(text: string) => void>(() => {});
export const useToast = () => useContext(Ctx);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<T[]>([]);
  const n = useRef(0);
  const dismiss = (id: number) => setItems((s) => s.filter((x) => x.id !== id));
  const push = useCallback((text: string) => {
    const id = ++n.current;
    setItems([{ id, text }]);
    setTimeout(() => setItems((s) => s.filter((x) => x.id !== id)), 5000);
  }, []);
  return (
    <Ctx.Provider value={push}>
      {children}
      <div className="toast-host" role="status" aria-live="polite">
        {items.map((t) => <div key={t.id} className="toast animate-rise"><span>{t.text}</span><IconButton label="إغلاق التنبيه" onClick={() => dismiss(t.id)}><XIcon size={20} /></IconButton></div>)}
      </div>
    </Ctx.Provider>
  );
}
