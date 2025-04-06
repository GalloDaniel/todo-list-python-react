export async function setAuth(username, password) {
  const response = await fetch("http://localhost:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      username,
      password
    })
  })

  return response;
}

export async function fetchTodos(token) {
  const res = await fetch("http://localhost:8000/todos", {
    headers: { Authorization: `Basic ${token}` }
  });
  return res;
}

export async function createTodo(todo, token) {
  const res = await fetch("http://localhost:8000/todos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${token}`
    },
    body: JSON.stringify(todo)
  });
  return res.json();
}

export async function updateTodo(id, todo, token) {
  const res = await fetch(`http://localhost:8000/todos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${token}`
    },
    body: JSON.stringify(todo)
  });
  return res.json();
}

export async function deleteTodo(id, token) {
  await fetch(`http://localhost:8000/todos/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Basic ${token}` }
  });
}
