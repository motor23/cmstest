import React from 'react';


class Application extends React.Component {
    static childContextTypes = {
        connection: React.PropTypes.object.isRequired,
    };

    getChildContext() {
        return {
            connection: this.props.connection
        }
    }

    render() {
        let {children} = this.props;
        console.log(this.props);
        return (
            <div className="mdl-layout">
                {children}
            </div>
        );
    }
}


export default Application;