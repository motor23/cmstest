import React, {Component, PropTypes} from 'react';


class Notifications extends Component {
    static propTypes = {
        isConnecting: PropTypes.bool.isRequired,
        isConnected: PropTypes.bool.isRequired,
        notifications: PropTypes.arrayOf(PropTypes.object).isRequired
    };

    render() {
        const {isConnecting, isConnected} = this.props;
        return (
            <div className="slds-notify_container">
                <div className="slds-notify slds-notify--alert">
                    <div className="slds-notify__content">

                    </div>
                </div>
            </div>
        );
    }
}


export default Notifications;