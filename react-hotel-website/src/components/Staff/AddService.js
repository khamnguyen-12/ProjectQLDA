/** @jsx jsx */
import { css, jsx } from '@emotion/react';
import { useState, useEffect } from 'react';
import Container from '../Global/Container';
import { authAPI, endpoints } from '../../configs/APIs';
import { SnackbarProvider, useSnackbar } from 'notistack';
import { Card, CardBody, CardTitle, CardText, Row, Col } from 'reactstrap';

const AddService = () => {
    const [nameService, setNameService] = useState('');
    const [price, setPrice] = useState(0);
    const [quantity, setQuantity] = useState(1);
    const [reservations, setReservations] = useState([]);
    const [services, setServices] = useState([]);
    const [selectedReservation, setSelectedReservation] = useState(null);
    const [selectedService, setSelectedService] = useState('');
    const [error, setError] = useState('');
    const [loadingReservations, setLoadingReservations] = useState(true);
    const [loadingServices, setLoadingServices] = useState(true);

    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        const fetchReservations = async () => {
            try {
                const response = await authAPI().get(endpoints['list_reservations']);
                setReservations(response.data);
            } catch (err) {
                setError('Failed to fetch reservations');
            } finally {
                setLoadingReservations(false);
            }
        };

        fetchReservations();
    }, []);

    useEffect(() => {
        const fetchServices = async () => {
            try {
                const response = await authAPI().get(endpoints['services']);
                setServices(response.data);
            } catch (err) {
                setError('Failed to fetch services');
            } finally {
                setLoadingServices(false);
            }
        };

        fetchServices();
    }, []);

    const handleServiceChange = (e) => {
        const selectedServiceId = e.target.value;
        const selectedService = services.find(service => service.id === parseInt(selectedServiceId));
        setSelectedService(selectedServiceId);
        setNameService(selectedService.nameService);
        setPrice(selectedService.price);
    };

    const handleQuantityChange = (e) => {
        const newQuantity = e.target.value;
        setQuantity(newQuantity);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const serviceData = {
            reservationId: selectedReservation,
            service: selectedService,
            quantity,
        };

        try {
            const response = await authAPI().post(endpoints['reservation_service'], serviceData);

            if (response.status === 201) {
                enqueueSnackbar('Dịch vụ đã được thêm thành công', { variant: 'success' });
                setNameService('');
                setPrice(0);
                setQuantity(1);
                setSelectedReservation(null);
                setSelectedService('');
            } else {
                enqueueSnackbar('Có lỗi xảy ra, vui lòng thử lại', { variant: 'error' });
            }
        } catch (error) {
            console.error('Error adding service:', error);
            enqueueSnackbar('Có lỗi xảy ra, vui lòng thử lại', { variant: 'error' });
        }
    };

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount);
    };

    return (
        <Container>
            <div css={styles}>
                <h1>Thêm dịch vụ</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Tên dịch vụ</label>
                        {loadingServices ? (
                            <p>Loading services...</p>
                        ) : (
                            <select
                                value={selectedService}
                                onChange={handleServiceChange}
                                required
                            >
                                <option value="">Chọn dịch vụ</option>
                                {services.map((service) => (
                                    <option key={service.id} value={service.id}>
                                        {service.nameService} - Giá: {formatCurrency(service.price)}
                                    </option>
                                ))}
                            </select>
                        )}
                        {error && <p>{error}</p>}
                    </div>
                    <div className="form-group">
                        <label>Số lượng</label>
                        <input
                            type="number"
                            value={quantity}
                            onChange={handleQuantityChange}
                            required
                            min="1"
                        />
                    </div>

                    <div className="form-group">
                        <label>Tổng phí dịch vụ</label>
                        <input
                            type="text"
                            value={formatCurrency(price * quantity)}
                            readOnly
                        />
                    </div>

                    <div className="form-group">
                        <label>Chọn phiếu đặt phòng</label>
                        {loadingReservations ? (
                            <p>Loading reservations...</p>
                        ) : (
                            <select
                                value={selectedReservation}
                                onChange={(e) => setSelectedReservation(e.target.value)}
                                required
                            >
                                <option value="">Chọn phiếu</option>
                                {reservations.map((reservation) => (
                                    <option key={reservation.id} value={reservation.id}>
                                        {reservation.guest} - {reservation.room.map(r => r.nameRoom).join(', ')}
                                    </option>
                                ))}
                            </select>
                        )}
                        {error && <p>{error}</p>}
                    </div>
                    <button type="submit">Thêm dịch vụ</button>
                </form>
                <ServiceList />
            </div>
        </Container>
    );
};

const styles = css`
    padding: 20px;
    background-color: #f9f9f9;
    h1 {
        margin-bottom: 20px;
    }
    .form-group {
        margin-bottom: 15px;
        label {
            display: block;
            margin-bottom: 5px;
        }
        input, select {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
    }
    button {
        padding: 10px 20px;
        background-color: #0000cd;
        color: #fff;
        border: none;
        cursor: pointer;
        &:hover {
            background-color: #00008b;
        }
    }
    p {
        margin-top: 15px;
        color: #ff1414;
    }
`;

const ServiceList = () => {
    const [services, setServices] = useState([]);

    useEffect(() => {
        const fetchServices = async () => {
            try {
                const response = await authAPI().get(endpoints['reservation_service']);
                setServices(response.data);
                console.log('API response status:', response.status);
                console.log('API response data:', response.data);
            } catch (error) {
                console.error('Error fetching services:', error);
            }
        };

        fetchServices();
    }, []);

    // Group services by guest and room
    const groupedServices = services.reduce((acc, service) => {
        const key = `${service.guest_name} - Phòng: ${service.room_names}`;
        if (!acc[key]) {
            acc[key] = [];
        }
        acc[key].push(service);
        return acc;
    }, {});

    return (
        <Container>
            <div css={listStyles}>
                <h1>Danh sách phiếu đặt phòng</h1>
                {Object.entries(groupedServices).map(([key, services]) => (
                    <div key={key} css={groupStyle}>
                        <h2 css={groupTitleStyle}>{key}</h2>
                        <Row>
                            {services.map((service, index) => (
                                <Col key={index} sm="12" md="6" lg="4">
                                    <Card css={cardStyle}>
                                        <CardBody>
                                            <CardTitle tag="h5" css={cardTitleStyle}>{service.service_name}</CardTitle>
                                            <CardText css={cardTextStyle}>
                                                Dịch vụ: {service.nameService} <br />
                                                Giá: {service.price.toLocaleString()} VND<br />
                                                Số lượng: {service.quantity}
                                            </CardText>
                                        </CardBody>
                                    </Card>
                                </Col>
                            ))}
                        </Row>
                    </div>
                ))}
            </div>
        </Container>
    );
};

const listStyles = css`
    padding: 20px;
    background-color: #f9f9f9;
    h1 {
        margin-bottom: 20px;
        text-align: center;
    }
`;

const groupStyle = css`
    margin-bottom: 20px;
    padding: 10px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const groupTitleStyle = css`
    font-size: 1.25rem;
    color: #343a40;
    margin-bottom: 10px;
`;

const cardStyle = css`
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    &:hover {
        transform: scale(1.05);
    }
`;

const cardTitleStyle = css`
    font-size: 1rem;
    color: #007bff;
`;

const cardTextStyle = css`
    font-size: 0.875rem;
    color: #343a40;
`;

export default () => (
    <SnackbarProvider maxSnack={3}>
        <AddService />
    </SnackbarProvider>
);
