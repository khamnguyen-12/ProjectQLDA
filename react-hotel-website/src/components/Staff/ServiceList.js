/** @jsx jsx */
import { css, jsx } from '@emotion/react';
import { useState, useEffect } from 'react';
import Container from '../Global/Container';
import { authAPI, endpoints } from '../../configs/APIs';
import { Card, CardBody, CardTitle, CardSubtitle, CardText, Row, Col } from 'reactstrap';

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
            <div css={styles}>
                <h1>Danh sách dịch vụ</h1>
                {Object.entries(groupedServices).map(([key, services]) => (
                    <div key={key} css={groupStyle}>
                        <h2 css={groupTitleStyle}>{key}</h2>
                        <Row>
                            {services.map((service, index) => (
                                <Col key={index} sm="12" md="6" lg="4">
                                    <Card css={cardStyle}>
                                        <CardBody>
                                            <CardTitle tag="h5" css={cardTitleStyle}>{service.service}</CardTitle>
                                            <CardText css={cardTextStyle}>
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

const styles = css`
    padding: 40px;
    background-color: #f9f9f9;
    h1 {
        margin-bottom: 40px;
        text-align: center;
    }
`;

const groupStyle = css`
    margin-bottom: 40px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const groupTitleStyle = css`
    font-size: 1.75rem;
    color: #343a40;
    margin-bottom: 20px;
`;

const cardStyle = css`
    margin-bottom: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    &:hover {
        transform: scale(1.05);
    }
`;

const cardTitleStyle = css`
    font-size: 1.25rem;
    color: #007bff;
`;

const cardTextStyle = css`
    font-size: 1rem;
    color: #343a40;
`;

export default ServiceList;
