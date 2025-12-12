import ReportModal from "./ReportModal/ReportModal";
import TrackModal from "./TrackModal/TrackModal";
import SupportModal from "./SupportModal/SupportModal";
import ModalComponent from "../../../component/Modals/ModalComponent";


const ModalForContent = ({ popupType, togglePopup, closePopup }: { popupType: string, togglePopup: boolean, closePopup:any }) => {
    // let footerBtns:ReactNode

    // switch (popupType) {
    //     case "reoport":
            
    //         break;
    
    //     default:
    //         break;
    // }

    return (
        <ModalComponent open={togglePopup} onClose={closePopup} footer={[]} width="765px" maskClosable={popupType === "report" && false}>
            {popupType === "report" && <ReportModal/>}
            {popupType === "track" && <TrackModal/>}
            {popupType === "support" && <SupportModal/>}
        </ModalComponent>
    )
}

export default ModalForContent