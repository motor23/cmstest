import React, {Component, PropTypes} from 'react'
import paginate from '.../util';


export class Paginator extends Component {
    static propTypes = {
        total: PropTypes.number.isRequired,
        page: PropTypes.number.isRequired,
        pageSize: PropTypes.number.isRequired,
        change: PropTypes.func.isRequired
    };

    renderItem(n) {
        const {page, change} = this.props;
        if (n === page) {
            return (
                <span key={n} className="cms-paginator__item cms-paginator__item--current">
                    {n}
                </span>
            );
        }
        if (n === null) {
            return (
                <span className="cms-paginator__item cms-paginator__item--ellipsis">
                    &hellip;
                </span>
            );
        }
        return (
            <span key={n} className="cms-paginator__item" onClick={() => change(n)}>
                {n}
            </span>
        );
    }

    render() {
        const {total, page, pageSize} = this.props;
        const pages = paginate(total, pageSize, page, 1, 3);
        return (
            <div className="cms-paginator">
                {pages.map(this.renderItem.bind(this))}
            </div>
        );
    }
}