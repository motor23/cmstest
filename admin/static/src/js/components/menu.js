import React from 'react';
import {Link} from 'react-router';


class MenuStream extends React.Component {
    static propTypes = {
        children: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
        title: React.PropTypes.string.isRequired,
        stream: React.PropTypes.string.isRequired
    };

    render() {
        const {children, title, stream} = this.props;
        return (
            <div className="cms-nav__item">
                <a href={`/${stream}/`}>{title}</a>
            </div>
        );
    }
}


class MenuLink extends React.Component {
    static propTypes = {
        children: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
        title: React.PropTypes.string.isRequired,
        url: React.PropTypes.string.isRequired
    };

    render() {
        const {children, title, url} = this.props;
        return (
            <div className="cms-nav__item">
                <a href={url}>{title}</a>
            </div>
        );
    }
}



function render(item, registry) {
    const element = registry[item.widget];
    const instance = React.createElement(element, {});
}


class Menu extends React.Component {
    static propTypes = {
        menu: React.PropTypes.arrayOf(React.PropTypes.object).isRequired
    };

    render() {
        return (
            <div className="cms-nav">
                <div className="cms-nav__item">
                    <Link to="/" activeClassName="active">Начало</Link>
                </div>
                <div className="cms-nav__item">
                    <Link to="/materials/" activeClassName="active">Материалы</Link>
                </div>
                <div className="cms-nav__item">
                    <Link to="/multimedia/" activeClassName="active">Мультимедиа</Link>
                </div>
            </div>
        );
    }
}


export default Menu;