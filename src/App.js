import React from "react";
import Home from "./src/Home";
import Refresh from "./src/Refresh";
import Return from "./src/Return";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./src/App.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/refresh/:connectedAccountId",
    element: <Refresh />,
  },
  {
    path: "/return/:connectedAccountId",
    element: <Return />,
  },
]);

export default function App() {
  return (
    <div>
      <RouterProvider router={router} />
    </div>
  );
}
