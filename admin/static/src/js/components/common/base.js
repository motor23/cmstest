import React, {Component} from 'react'


class Base extends Component {
    render() {
        return (
            <div className="mdl-layout mdl-layout--fixed-header">
                <div className="mdl-layout__header">
                    <div className="mdl-layout__header-row">
                    </div>
                </div>
                <div className="mdl-layout__content mdl-color-text--grey-600">
                    {cloneElement(children, props)}
                </div>
            </div>
        );
    }
}