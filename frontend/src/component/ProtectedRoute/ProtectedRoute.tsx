import { Outlet } from "react-router-dom"


const ProtectedRoute = () => {
    // Restrict certain pages to user not logged in
    return <Outlet/>
}

export default ProtectedRoute