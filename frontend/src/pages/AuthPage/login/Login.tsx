import CompanyName from "../../../component/CompanyName/CompanyName"
import loginonBoardingImg from "../../../assets/loginOnboardingImg.svg"
import AuthInput from "../../../component/authInput/AuthInput"
import { HiOutlineMail } from "react-icons/hi";
import { RxEyeOpen } from "react-icons/rx";
import { FcGoogle } from "react-icons/fc";
import { GoEyeClosed } from "react-icons/go";
import { useState } from "react";
import { GoogleLogin, useGoogleLogin } from '@react-oauth/google';


const Login = () => {

  const [toggleShowPassword, setToggleShowPassword] = useState<boolean>(false)

  const loginForm = [
    {
      name: "email",
      label: "Email",
      inputType: "email",
      placeholder: "johndoe@email.com",
      required: true,
      icon: <HiOutlineMail />
    },

    {
      name: "password",
      label: "Password",
      inputType: toggleShowPassword ? "text" : "password",
      placeholder: "********",
      required: true,
      icon: toggleShowPassword ? <RxEyeOpen /> : <GoEyeClosed />
    },
  ]

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: (tokenResponse) => {
      // call the api for sending token to backend
      console.log(tokenResponse)
    },
    onError: () => {
      console.log("Login Failed")
    },
    
  })

  return (
    <main className="w-screen min-h-screen flex flex-row justify-between bg-[#F2F9FF]">
      <section className="w-[45%] flex flex-col space-y-8 items-center justify-center px-[50px]">
        <div className="text-center">
          <CompanyName className="font-semibold" />
          <p className="text-lg text-black/70">Welcome back -  you're in a <span className="underline decoration-[#7B89CE]">safe space</span></p>
        </div>

        <div className="bg-white rounded-xl shadow-lg px-6 py-8 w-full">
          <form className="">
            <section className="flex flex-col space-y-6">
              {loginForm.map((each, index) => (
                <div key={index} className="">
                  <AuthInput
                    name={each.name}
                    inputType={each.inputType}
                    placeholder={each.placeholder}
                    label={each.label}
                    required={each.required}
                  >

                    {/* Icon */}
                    <div onClick={() => { each.name === "password" && setToggleShowPassword((prev) => !prev) }}>
                      {each.icon}
                    </div>

                  </AuthInput>
                </div>
              ))}
            </section>

            <section>
              <p className="cursor-pointer text-sm mt-2">Forgot Password?</p>
            </section>

            <section className="w-full flex flex-col space-y-4 mt-8">
              <button className="bg-primaryBlue-300 rounded-xl text-white py-3 text-lg cursor-pointer hover:opacity-70 hover:translate-y-0.5 hover:transition-all hover:duration-200">Log in</button>
            </section>


          </form>

          <button className="bg-[#F1F1F1] rounded-xl text-black py-3 text-lg cursor-pointer hover:translate-y-0.5  hover:transition-all hover:duration-200 flex flex-row space-x-2 items-center justify-center w-full mt-4" onClick={() => handleGoogleLogin()}>
            <FcGoogle className="text-2xl"/>
            <p>Sign in with google</p>
          </button>

          <section>
            <p className="mt-6 text-center">Don't have an account? <span className="underline font-semibold decoration-primaryBlue-300 text-primaryBlue-300">Sign Up</span></p>
          </section>
        </div>
      </section>


      <section className="max-w-[55%] h-screen ">
        <img src={loginonBoardingImg} alt="" className="h-screen rounded-tl-[20%] rounded-bl-[20%]" />
      </section>
    </main>
  )
}

export default Login