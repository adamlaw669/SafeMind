import { type ReactNode } from 'react';
import { Modal } from 'antd';


type ModalComponentProps = {
    children: ReactNode;
    footer: ReactNode;
    open: boolean;
    onClose: ()=>void;
    title?: string
}

const ModalComponent = ({ children, footer, open, onClose, title }: ModalComponentProps) => {
    
    return (
        <>
            <Modal
                title={title}
                closable={{ 'aria-label': 'Custom Close Button' }}
                open={open}
                onOk={onClose}
                onCancel={onClose}
                footer={footer || []}
                width="765px"
            >
                {children}
            </Modal>
        </>
    );
};

export default ModalComponent;