import footerLogo from "../../assets/footerLogo.svg"
import { IoLogoInstagram } from "react-icons/io";
import { BsTwitterX } from "react-icons/bs";
import { ImLinkedin2 } from "react-icons/im";
import { FaFacebook } from "react-icons/fa";
import LandingPgButton from "../LandingPgButtonStyles/LandingPgButton";


const Footer = () => {
    return (
        <footer className="w-full bg-[#292F67] py-5 flex justify-between px-6 md:px-16">
            <section>
                <img src={footerLogo} alt="safemind - Your voice matters — and so does your peace!" className="w-36 h-36" />
            </section>

            <section className="flex flex-col space-y-4 justify-between">
                <h1 className="text-white font-semibold">Contact Us</h1>

                <div className="text-white/70 space-y-2 text-[15px]">
                    <p>7, Unilag Rd, Akoka, Lagos</p>
                    <p>(+234)-999-7777-888</p>
                    <p>7, Unilag Rd, Akoka, Lagos</p>
                </div>

                <div className="flex items-center space-x-3">
                    <IoLogoInstagram className="text-white text-xl cursor-pointer hover:scale-110 hover:transition-all hover:duration-200" />
                    <BsTwitterX className="text-white text-lg cursor-pointer hover:scale-110 hover:transition-all hover:duration-200" />
                    <ImLinkedin2 className="text-white text-lg cursor-pointer hover:scale-110 hover:transition-all hover:duration-200" />
                    <FaFacebook className="text-white text-lg cursor-pointer hover:scale-110 hover:transition-all hover:duration-200" />
                </div>
            </section>


            <section className="flex flex-col space-y-4">
                <h1 className="text-white font-semibold">Quick Links</h1>

                <ul className="text-white/70 space-y-2 text-[15px]">
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">About Us</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Healing starts here</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Our Initiatives</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Get Involved</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Become a donor</li>
                </ul>
            </section>


            <section className="flex flex-col space-y-4">
                <h1 className="text-white font-semibold">Company</h1>
                <ul className="text-white/70 space-y-2 text-[15px]">
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Become a Partner</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Resources</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Stories</li>
                    <li className="cursor-pointer hover:text-white hover:transition-all duration-200">Events</li>
                </ul>
            </section>

             <section className="flex flex-col space-y-4">
                <h1 className="text-white font-semibold text-center">Donate</h1>

                <LandingPgButton className="bg-transparent border border-white/80 text-white px-16 py-2" onClick={()=>{}}>
                    <p>Donate</p>
                </LandingPgButton>
            </section>
        </footer>
    )
}

export default Footer