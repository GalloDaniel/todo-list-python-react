import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./Login";
import TodoList from "./TodoList";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/todos" element={<TodoList />} />
      </Routes>
    </Router>
  );
}

export default App;
