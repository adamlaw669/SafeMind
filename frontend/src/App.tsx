import { useRoutes } from "react-router-dom"
import { route } from "./routes/route"

function App() {

  const routing = useRoutes(route)

  return routing

}

export default App
