import ReportModal from "./ReportModal/ReportModal";
import TrackModal from "./TrackModal/TrackModal";
import SupportModal from "./SupportModal/SupportModal";
import ModalComponent from "../../../component/Modals/ModalComponent";
import type { ReactNode } from "react";

const ModalForContent = ({ popupType, togglePopup, closePopup }: { popupType: string, togglePopup: boolean, closePopup:any }) => {
    // let footerBtns:ReactNode

    // switch (popupType) {
    //     case "reoport":
            
    //         break;
    
    //     default:
    //         break;
    // }

    return (
        <ModalComponent open={togglePopup} onClose={closePopup} footer={[]}>
            {popupType === "report" && <ReportModal/>}
            {popupType === "track" && <TrackModal/>}
            {popupType === "support" && <SupportModal/>}
        </ModalComponent>
    )
}

export default ModalForContent