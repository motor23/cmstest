import React from 'react';


class Dashboard extends React.Component {
    render() {
        return (
            <div>
                <div className="mdl-card">
                    <div className="mdl-card__title">Главная страница</div>
                    <div className="mdl-card__actions mdl-card--border">
                        <button className="mdl-button mdl-js-button">Ленты</button><br/>
                        <button className="mdl-button mdl-js-button">Важное</button><br/>
                        <button className="mdl-button mdl-js-button">Слайдер</button><br/>
                        <button className="mdl-button mdl-js-button">Хайлайт</button><br/>
                        <button className="mdl-button mdl-js-button">Мультимедиа</button><br/>
                        <button className="mdl-button mdl-js-button">Баннеры</button><br/>
                    </div>
                </div>
                <div className="mdl-card">
                    <div className="mdl-card__title">Материалы</div>
                    <div className="mdl-card__actions mdl-card--border">
                        <button className="mdl-button mdl-js-button">Документы</button><br/>
                        <button className="mdl-button mdl-js-button">Глоссарий</button><br/>
                        <button className="mdl-button mdl-js-button">Персоны</button><br/>
                        <button className="mdl-button mdl-js-button">Институты</button><br/>
                        <button className="mdl-button mdl-js-button">pravo.gov.ru</button><br/>
                    </div>
                </div>
            </div>
        );
    }
}


export default Dashboard;