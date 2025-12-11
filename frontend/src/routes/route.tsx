import type { RouteObject } from "react-router-dom";
import Landing from "../pages/Landing/Landing";
import Login from "../pages/AuthPage/login/Login";
import Signup from "../pages/AuthPage/signup/Signup";
import ProtectedRoute from "../component/ProtectedRoute/ProtectedRoute";
import AgencyDashboard from "../pages/UserDashboard/AgencyDashboard";


export const route: RouteObject[] = [
    {
        path: '/',
        element: <Landing/>
    },
    {
        path: '/login',
        element: <Login/>
    },
    {
        path: '/register',
        element: <Signup/>
    },

    // Protected Routes
    {
        element: <ProtectedRoute/>,
        children: [
            {
                path: '/dashboard',
                element: <AgencyDashboard/>
            }
        ]
    }
]