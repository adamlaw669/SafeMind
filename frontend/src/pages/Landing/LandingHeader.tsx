import headerImg from "../../assets/landingPg-headerImg.png"
import LandingPgButton from "../../component/LandingPgButtonStyles/LandingPgButton"

const LandingHeader = () => {
  return (
    <header className='flex flex-col space-y-8 md:space-y-0 md:flex-row justify-between min-h-[calc(100vh-5rem)] items-center'>
      {/* Text */}
      <section className="md:w-[50%] flex flex-col space-y-8">
        <h1 className=" text-black text-3xl text-center md:text-left md:text-[40px] font-semibold">
          Your <span className="text-primaryBlue-300"> voice</span> matters &mdash; and so does your <span className="text-primaryBlue-300"> peace!</span>
        </h1>

        <p className="text-lg font-sans ">
          Whether you're facing abuse, injustice, or harm — SafeMind gives you a secure
          and confidential space to report your experience, find real support,
          and begin healing at your own pace.
        </p>

        <div className="flex flex-col w-full space-y-4 md:space-y-0 md:flex-row md:space-x-5 items-center">
          <LandingPgButton onClick={() => console.log("a")} className=" bg-primaryBlue-300 text-white px-6 hover:bg-transparent hover:border hover:border-primaryBlue-300 w-full hover:text-primaryBlue-300">
            <p className="font-normal">Join the Community</p>
          </LandingPgButton>
          
          <LandingPgButton onClick={() => console.log("a")} className="border border-primaryBlue-300 bg-transparent text-primaryBlue-300 hover:bg-primaryBlue-300 w-full hover:text-white">
            <p className="font-normal ">Report a Case</p>
          </LandingPgButton>
        </div>

      </section>

      {/* Image */}
      <section className="md:w-[40%]">
        <img src={headerImg} alt="your voice matters - safemind" className="w-full"/>
      </section>
    </header>
  )
}

export default LandingHeader