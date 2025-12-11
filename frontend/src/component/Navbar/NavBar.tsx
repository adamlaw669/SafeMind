import { NavLink } from "react-router-dom";
import logo from "../../assets/safemind-logo.svg"
import { FaBarsStaggered } from "react-icons/fa6";
import { useState } from "react";
import { HiXMark } from "react-icons/hi2";
import LandingPgButton from "../LandingPgButtonStyles/LandingPgButton";


const navLinks = [
  { label: "Home", linkTo: "/" },
  { label: "Report", linkTo: "/report" },
  { label: "Community", linkTo: "/community" },
  { label: "Emergency", linkTo: "/emergency" },
]

const NavBar = () => {
  const [toggleMobileNav, setToggleMobileNav] = useState<boolean>(false)

  return (
    <nav className="px-6 py-1 bg-[#F7F7F7] fixed z-50 w-full md:px-16">
      <div className="flex flex-row justify-between items-center w-full">
        <div>
          <img src={logo} alt="safemind logo" className="w-[80%]" />
        </div>

        <div className="md:hidden w-fit cursor-pointer" onClick={() => setToggleMobileNav((prev) => !prev)}>
          {!toggleMobileNav && <FaBarsStaggered className="text-lg text-primaryBlue-300" />}
          {toggleMobileNav && <HiXMark className="text-2xl text-primaryBlue-300" />}
        </div>


        {/* Desktop nav links */}

        <ul className="hidden md:flex md:flex-row md:space-x-12">
          {navLinks.map((navLink, idx) => (
            <NavLink to={navLink.linkTo} key={idx}>
              <li className={`${navLink.linkTo === "/emergency" && "text-red-500"}`}>{navLink.label}</li>
            </NavLink>

          ))}
        </ul>


        <div className="hidden md:flex space-x-5">
          <LandingPgButton onClick={() => console.log("a")} className="border border-primaryBlue-300 bg-transparent text-primaryBlue-300 hover:bg-primaryBlue-300 hover:text-white">
            <p className="font-normal ">Sign in</p>
          </LandingPgButton>

          <LandingPgButton onClick={() => console.log("a")} className=" bg-primaryBlue-300 text-white px-6 hover:bg-transparent hover:border hover:border-primaryBlue-300 hover:text-primaryBlue-300">
            <p className="font-normal ">Login</p>
          </LandingPgButton>
        </div>
      </div>

      {/* Desktop navlinks end */}



      {/* Mobile nav links */}
      {toggleMobileNav && (
        <div className={`mt-3`}>
          <div>
            <ul className="flex flex-col space-y-3">
              {navLinks.map((navLink, idx) => (
                <NavLink to={navLink.linkTo} key={idx}>
                  <li>{navLink.label}</li>
                </NavLink>

              ))}
            </ul>
          </div>

          <div className="flex space-x-5 items-center mt-5 mb-3">
            <LandingPgButton onClick={() => console.log("a")} className="border border-primaryBlue-300 bg-transparent text-primaryBlue-300 hover:bg-primaryBlue-300 hover:text-white px-5">
              <p className="font-normal ">Sign in</p>
            </LandingPgButton>

            <LandingPgButton onClick={() => console.log("a")} className=" bg-primaryBlue-300 text-white px-6 hover:bg-transparent hover:border hover:border-primaryBlue-300 hover:text-primaryBlue-300">
              <p className="font-normal">Login</p>
            </LandingPgButton>
          </div>
        </div>
      )}


    </nav>
  )
}

export default NavBar