import React from 'react';
import { Select, Space, type SelectProps } from 'antd';

const SelectFieldComponent: React.FC<SelectProps> = ({options, defaultValue, onChange, value}) => (
    <Space wrap>
        <Select
            defaultValue={defaultValue}
            style={{ minWidth: 337.5,  minHeight: 60 }}
            onChange={onChange}
            value={value === undefined ? defaultValue : value}
            options={options}
        />
    </Space>
);

export default SelectFieldComponent;