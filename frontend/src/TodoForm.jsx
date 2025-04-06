import { useState } from "react";
import { createTodo, updateTodo } from "./api";

export default function TodoForm({ refresh, todo = null }) {
  const [title, setTitle] = useState(todo?.title || "");
  const [description, setDescription] = useState(todo?.description || "");
  const [completed, setCompleted] = useState(todo?.completed || false);
  const [error, setError] = useState("");


  const handleSubmit = async () => {
    setError("");
    const data = { title, description, completed };
    let response;
    if (todo) {
      response = await updateTodo(todo.id, data, localStorage.getItem("token"));
    } else {
      response = await createTodo(data, localStorage.getItem("token"));
    }

    if (response.detail) {
      console.log(response)
      const errorMessage = response.detail.map(e => e.msg).join(" | ");
      setError(errorMessage || "An error occurred");
      return;
    }

    refresh();
  };

  return (
    <div>
      <input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
      <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
      <label>
        Completed
        <input type="checkbox" checked={completed} onChange={e => setCompleted(e.target.checked)} />
      </label>
      <button onClick={handleSubmit}>{todo ? "Update" : "Create"}</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
