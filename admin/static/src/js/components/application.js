import React from 'react';


class Application extends React.Component {
    render() {
        let {children} = this.props;
        return (
            <div className="mdl-layout">
                {children}
            </div>
        );
    }
}


export default Application;