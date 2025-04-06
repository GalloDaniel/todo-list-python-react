import { useEffect, useState, useCallback } from "react";
import { fetchTodos, deleteTodo } from "./api";
import { useNavigate } from "react-router-dom";
import TodoForm from "./TodoForm";

export default function TodoList() {
  const navigate = useNavigate();
  const [todos, setTodos] = useState([]);
  const [editing, setEditing] = useState(null);

  const load = useCallback(async () => {
    try {
      const data = await fetchTodos(localStorage.getItem("token"));

      if (data.ok) {
        const todos = await data.json();
        setTodos(todos);
        setEditing(null);
      } else if (data.status === 404) {
        console.error("Todos not found");
      } else {
        navigate("/");
      }
    } catch (error) {
      console.error("Token verification error:", error);
      localStorage.removeItem("token");
      navigate("/");
    }
  }, [navigate]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div>
      <h2>Todos</h2>
      <TodoForm refresh={load} />
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <strong>{todo.title}</strong> - {todo.description} [{todo.completed ? "✔" : "❌"}]
            <button onClick={() => setEditing(todo)}>Edit</button>
            <button onClick={async () => { await deleteTodo(todo.id, localStorage.getItem("token")); load(); }}>Delete</button>
          </li>
        ))}
      </ul>
      {editing && (
        <div>
          <h3>Edit Todo</h3>
          <TodoForm todo={editing} refresh={load} />
        </div>
      )}
    </div>
  );
}
