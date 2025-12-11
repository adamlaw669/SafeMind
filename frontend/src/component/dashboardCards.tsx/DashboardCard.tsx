import type { ReactElement } from "react";

type DashBoardCardPropsType = {
    className?: string;
    children: ReactElement
}

const DashboardCard = ({className, children} : DashBoardCardPropsType) => {
  return (
    <section className={`${className} bg-[#FAFAFA] rounded-2xl px-2 py-4 shadow-md`}>
        {children}
    </section>
  )
}

export default DashboardCard