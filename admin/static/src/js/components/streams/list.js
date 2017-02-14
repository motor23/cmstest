import React, {Component, PropTypes} from 'react';
import paginate from '../../util/paginate';
import Spinner from '../common/spinner';


export class StreamListRow extends Component {
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


export class StreamList extends Component {
    static propTypes = {
        actions: PropTypes.object.isRequired,
        isLoading: PropTypes.bool.isRequired,
        filters: PropTypes.object.isRequired,
        errors: PropTypes.object.isRequired,
        items: PropTypes.arrayOf(PropTypes.object).isRequired,
        total: PropTypes.number.isRequired,
        pageSize: PropTypes.number.isRequired,
        page: PropTypes.number.isRequired
    };

    componentWillMount() {
        const {stream, page, pageSize, actions} = this.props;
        actions.streamList({stream, page, pageSize});
    }

    changePage(page) {
        const {pageSize} = this.props;
        this.props.dispatch(updateStreamList('docs', page, pageSize));
    }

    render() {
        const {isLoading, title, items, total, pageSize, page} = this.props;
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
                <Paginator total={total} page={page} pageSize={pageSize} change={this.changePage.bind(this)}/>
            </div>
        );
    }
}