import React, {Component, PropTypes} from 'react';
import Spinner from '../common/spinner';


export class Waiting extends Component {
    reload(event) {
        window.location.reload(true);
    }

    render() {
        const {children, shouldReloadPage} = this.props;
        return (
            <div className="slds-modal slds-fade-in-open">
                <div className="slds-modal__container">
                    {shouldReloadPage ?
                        <div>
                            <button className="slds-button" onClick={this.reload}>
                                <svg className="slds-icon sld-icon--small">
                                    <path d="M21.5 1.8h-1.4c-.4 0-.7.4-.7.7v3.3c0 .4-.2.6-.6.3-.1-.2-.2-.3-.4-.5-2.3-2.3-5.6-3.2-8.9-2.6-1.1.2-2.3.7-3.2 1.3-2.8 1.9-4.5 4.9-4.5 8.1 0 2.5.9 5 2.7 6.8 1.8 1.9 4.3 3 7 3 2.3 0 4.6-.8 6.3-2.3.3-.3.3-.7.1-1l-1-1c-.2-.2-.7-.3-.9 0-1.7 1.3-4 1.9-6.2 1.3-.6-.1-1.2-.4-1.8-.7-2.6-1.6-3.8-4.7-3.1-7.7.1-.6.4-1.2.7-1.8 1.3-2.2 3.6-3.5 6-3.5 1.8 0 3.6.8 4.9 2.1.2.2.4.4.5.6.2.4-.2.6-.6.6h-3.2c-.4 0-.7.3-.7.7v1.4c0 .4.3.6.7.6h8.4c.3 0 .6-.2.6-.6V2.5c0-.3-.4-.7-.7-.7z"/>
                                </svg>
                            </button>
                            <div>Для продолжения работы требуется перезагрузить страницу</div>
                        </div>
                        :
                        <div>
                            <Spinner/>
                            {children}
                        </div>
                    }
                </div>
            </div>
        );
    }
}