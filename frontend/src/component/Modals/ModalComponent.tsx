import { type ReactNode } from 'react';
import { Modal } from 'antd';


type ModalComponentProps = {
    children: ReactNode;
    footer: ReactNode;
    open: boolean;
    onClose: ()=>void;
    title?: string;
    width?: string;
    maskClosable?: boolean
}

const ModalComponent = ({ children, footer, open, onClose, title, width, maskClosable }: ModalComponentProps) => {
    
    return (
        <>
            <Modal
                title={title}
                closable={{ 'aria-label': 'Custom Close Button' }}
                open={open}
                onOk={onClose}
                onCancel={onClose}
                footer={footer || []}
                width={width}
                maskClosable={maskClosable}
            >
                {children}
            </Modal>
        </>
    );
};

export default ModalComponent;