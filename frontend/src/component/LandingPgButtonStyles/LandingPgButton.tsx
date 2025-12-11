import type { ReactElement } from "react"

type LandingPgButtonProps = {
    icon?: ReactElement;
    children:ReactElement;
    className?: string;
    onClick: ()=>void;
}

const LandingPgButton = ({children, icon, className, onClick} : LandingPgButtonProps) => {
  return (
    <button className={`${className} w-fit rounded-full px-3 py-2 cursor-pointer font-semibold text-center flex flex-row justify-center items-center hover:transition-all hover:duration-200`} onClick={onClick}>
        {children}
    </button>
  )
}

export default LandingPgButton