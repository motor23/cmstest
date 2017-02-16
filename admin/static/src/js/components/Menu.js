import React, {Component, PropTypes, createElement} from 'react';
import {Link} from 'react-router';
import logger from '../util/log';


export class MenuItemStream extends Component {
    static propTypes = {
        title: PropTypes.string.isRequired,
        stream: PropTypes.string.isRequired,
        children: PropTypes.array.isRequired,
        parent: PropTypes.func.isRequired
    };

    render() {
        const {title, stream, children, parent} = this.props;
        return (
            <li className="cms-nav__item">
                <Link className="cms-nav__title" to={`/streams/${stream}/`}>{title}</Link>
                {createElement(parent, {children})}
            </li>
        );
    }
}


export class MenuItemUrl extends Component {
    static propTypes = {
        title: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
        children: PropTypes.array.isRequired,
        parent: PropTypes.func.isRequired
    };

    render() {
        const {title, url, children, parent} = this.props;
        return (
            <li className="cms-nav__item">
                <a className="cms-nav__title" href={url} target="_blank">{title}</a>
                {createElement(parent, {children})}
            </li>
        );
    }
}


export class MenuItem extends Component {
    static propTypes = {
        title: PropTypes.string.isRequired,
        children: PropTypes.array.isRequired,
        parent: PropTypes.func.isRequired
    };

    render() {
        const {title, children, parent} = this.props;
        return (
            <li className="cms-nav__item">
                <span className="cms-nav__title">{title}</span>
                {createElement(parent, {children})}
            </li>
        );
    }
}


export default class Menu extends Component {
    static widgets = {
        'MenuItem_Stream': MenuItemStream,
        'MenuItem_Url': MenuItemUrl,
        'MenuItem': MenuItem
    };

    static propTypes = {
        children: PropTypes.arrayOf(PropTypes.shape({
            title: PropTypes.string.isRequired,
            children: PropTypes.array.isRequired,
            widget: PropTypes.string.isRequired
        })).isRequired
    };

    render() {
        const {children} = this.props;
        const {widgets} = this.constructor;
        if (children && children.length) {
            return (
                <ul className="cms-nav">
                    {children.map(props => {
                        const parent = this.constructor;
                        const widget = widgets[props.widget];
                        logger.assert(widget, 'Widget not found: %s', props.widget);
                        return createElement(widget, {...props, parent});
                    })}
                </ul>
            );
        }
        return null;
    }
}