import React from 'react';
import {connect} from 'react-redux';
import {updateStreamList} from '../../actions';
import paginate from '../../util/paginate';
import Spinner from '../spinner';


class Paginator extends React.Component {
    static propTypes = {
        total: React.PropTypes.number.isRequired,
        limit: React.PropTypes.number.isRequired,
        offset: React.PropTypes.number.isRequired,
        change: React.PropTypes.func.isRequired
    };

    renderItem(page) {
        const {limit, offset, change} = this.props;
        const currentPage = Math.ceil(offset / limit + 1);
        if (page == currentPage) {
            return (
                <span className="cms-paginator__item cms-paginator__item--current">
                    {page}
                </span>
            );
        }
        if (page === null) {
            return (
                <span className="cms-paginator__item cms-paginator__item--ellipsis">
                    &hellip;
                </span>
            );
        }
        return (
            <span className="cms-paginator__item" onClick={() => change(page)}>
                {page}
            </span>
        );
    }

    render() {
        const {total, limit, offset} = this.props;
        const page = Math.ceil(offset / limit + 1);
        const pages = paginate(total, limit, page, 1, 3);
        return (
            <div className="cms-paginator">
                {pages.map(this.renderItem.bind(this))}
            </div>
        );
    }
}


class StreamListRow extends React.Component {
    render() {
        const {item} = this.props;
        return (
            <tr>
                <td>{item.id}</td>
                <td>{item.title.substring(0, 100)}</td>
            </tr>
        );
    }
}


class StreamList extends React.Component {
    static propTypes = {
        isLoading: React.PropTypes.bool.isRequired,
        widgets: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
        filters: React.PropTypes.object.isRequired,
        errors: React.PropTypes.object.isRequired,
        items: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
        total: React.PropTypes.number.isRequired,
        limit: React.PropTypes.number.isRequired,
        offset: React.PropTypes.number.isRequired
    };

    componentWillMount() {
        this.props.dispatch(updateStreamList('docs', 10));
    }

    changePage(page) {
        const {limit} = this.props;
        const offset = (page - 1) * limit;
        this.props.dispatch(updateStreamList('docs', limit, offset));
    }

    render() {
        const {isLoading, title, items, total, limit, offset} = this.props;
        const content = items.map(item => <StreamListRow key={item.id} item={item}/>);
        if (isLoading) {
            return <Spinner/>;
        }
        return (
            <div className="cms-stream">
                <div className="slds-page-header">
                    <div className="slds-page-header__title">{title}</div>
                </div>
                <table className="slds-table slds-table--bordered">
                    <thead>
                        <tr className="slds-text-heading--label">
                            <th>ID</th>
                            <th>Заголовок</th>
                        </tr>
                    </thead>
                    <tbody>
                    {content}
                    </tbody>
                </table>
                <Paginator total={total} limit={limit} offset={offset} change={this.changePage.bind(this)}/>
            </div>
        );
    }
}


function mapStateToProps(state, props) {
    return {
        isLoading: state.stream.isLoading,
        title: state.stream.title,
        items: state.stream.items,
        filters: state.stream.filters,
        errors: state.stream.errors,
        total: state.stream.total,
        limit: state.stream.limit,
        offset: state.stream.offset
    };
}


export default connect(mapStateToProps)(StreamList);