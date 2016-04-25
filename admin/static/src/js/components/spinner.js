import React from 'react'


class Spinner extends React.Component {
    componentDidMount() {
        window.componentHandler.upgradeDom();
    }

    componentDidUpdate() {
        window.componentHandler.upgradeDom();
    }

    render() {
        return (
            <div className="mdl-spinner mdl-spinner--single-color mdl-js-spinner is-active"/>
        );
    }
}


export default Spinner;