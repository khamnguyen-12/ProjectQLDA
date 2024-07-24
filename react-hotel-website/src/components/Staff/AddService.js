/** @jsx jsx */
import { css, jsx } from '@emotion/react';
import { useState, useEffect } from 'react';
import Container from '../Global/Container';
import { authAPI, endpoints } from '../../configs/APIs';
import { SnackbarProvider, useSnackbar } from 'notistack';

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
                <div css={reservationsStyle}>
                    <h2>Danh sách phiếu đặt phòng</h2>
                    <ul>
                        {reservations.map((reservation) => (
                            <li key={reservation.id}>
                                {reservation.guest} - Phòng: {reservation.room.map(r => r.nameRoom).join(', ')}
                                <button onClick={() => setSelectedReservation(reservation.id)}>
                                    Thêm dịch vụ
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </Container>
    );
};

const styles = css`
    padding: 120px;
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

const reservationsStyle = css`
    margin-top: 30px;
    h2 {
        margin-bottom: 15px;
    }
    ul {
        list-style-type: none;
        padding: 0;
        li {
            margin-bottom: 10px;
            button {
                margin-left: 10px;
                padding: 5px 10px;
                background-color: #007bff;
                border: none;
                color: #fff;
                cursor: pointer;
                &:hover {
                    background-color: #0056b3;
                }
            }
        }
    }
`;

export default () => (
    <SnackbarProvider maxSnack={3}>
        <AddService />
    </SnackbarProvider>
);
