import React from 'react'


class Spinner extends React.Component {
    render() {
        return (
            <div className="slds-spinner slds-spinner--small">
                <div className="slds-spinner__dot-a"></div>
                <div className="slds-spinner__dot-b"></div>
            </div>
        );
    }
}


export default Spinner;