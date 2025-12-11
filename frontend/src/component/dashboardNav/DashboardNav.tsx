import { FaX } from "react-icons/fa6";
import logo from "../../assets/logo-without-name.svg"
import { FaBars } from "react-icons/fa";
import CompanyName from "../CompanyName/CompanyName";
import { MdHome } from "react-icons/md";
import { TbProgressBolt } from "react-icons/tb";
import { IoChatbubbleEllipses } from "react-icons/io5";
import { IoMdSettings } from "react-icons/io";
import { NavLink } from "react-router-dom";
import { MdLogout } from "react-icons/md";
import { useState } from "react";
import { FaPeopleGroup } from "react-icons/fa6";



const DashboardNav = () => {
    const [toggleNav, setToggleNav] = useState<boolean>(false)

    const navLinks = [
        {
            label: "Dashboard",
            path: "/dashboard",
            icon: <MdHome />,
        },
        {
            label: "Safety Progress",
            path: "/safety-progress",
            icon: <TbProgressBolt />
        },
        {
            label: "Inbox",
            path: "/inbox",
            icon: <IoChatbubbleEllipses />
        },
        {
            label: "Community",
            path: "/community",
            icon: <FaPeopleGroup />
        },
        // {
        //     label: "Settings",
        //     path: "/settings",
        //     icon: <IoMdSettings />
        // },
    ]
    return (
        <nav className="fixed w-full lg:w-[300px] z-50">
            <section className="bg-[#C1C7E7] flex flex-row justify-between items-center px-4 lg:hidden">
                <div className="cursor-pointer">
                    <FaBars className="text-2xl" onClick={() => setToggleNav(true)} />
                </div>

                <div>
                    <img src={logo} alt="safemind-logo" />
                </div>
            </section>

            {/* Mobile NAv */}

            <section className={`absolute top-0 left-0 bg-[#F9F9F9] h-screen ${toggleNav ? "flex" : "hidden"} flex-col justify-between lg:justify-start px-2 items-center py-6 z-50 w-full lg:flex lg:w-full lg:rounded-r-[50px]`}>
                <div className="w-[80%]">
                    <FaX className="place-self-end text-primaryBlue-300 cursor-pointer lg:hidden" onClick={() => setToggleNav(false)} />
                    <div className="flex flex-row items-center justify-center">
                        <img src={logo} alt="safemind-logo" className="w-[53px]" />
                        <CompanyName className="text-[16px]" />
                    </div>
                </div>

                <div className="flex flex-col space-y-5 w-[80%] lg:mt-[65px] justify-end h-full">
                    {navLinks.map((navLink, idx) => (
                        <NavLink key={idx} to={navLink.path} className="dashboardNav flex flex-row space-x-[10px] justify-center items-center bg-[#F2F3F8] rounded-[20px] w-full text-black/70 py-2 shadow-md text-[16px] hover:-translate-y-0.5 hover:transition-all hover:duration-200 font-semibold
                        ">
                            <span className="text-xl">{navLink.icon}</span>
                            <h2>{navLink.label}</h2>
                        </NavLink>
                    ))}
                </div>

                <div className="w-[80%] flex flex-col space-y-4 h-full justify-end">
                    <NavLink to="/settings" className="dashboardNav flex flex-row space-x-[10px] justify-center items-center bg-[#F2F3F8] rounded-[20px] w-full text-black/70 py-2 shadow-md text-[16px] hover:-translate-y-0.5 hover:transition-all hover:duration-200 font-semibold">
                        <IoMdSettings />
                        <h2>Settings</h2>
                    </NavLink>

                    <button className="flex flex-row space-x-2 justify-center items-center bg-[#F2F3F8] rounded-[20px] w-full text-black/70 py-2 shadow-md text-[16px] hover:-translate-y-0.5 hover:transition-all hover:duration-200 font-semibold
                        ">
                        <h2>Logout</h2>
                        <span className="text-xl">
                            <MdLogout />
                        </span>
                    </button>
                </div>
            </section>

        </nav>
    )
}

export default DashboardNav