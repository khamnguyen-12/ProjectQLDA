/** @jsx jsx */
import { jsx, css } from '@emotion/react';
import { useState } from 'react';
import RoomCard from './RoomCard'; // Import component RoomCard

const MainContent = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [checkInDate, setCheckInDate] = useState('');
    const [checkOutDate, setCheckOutDate] = useState('');
    const [numGuests, setNumGuests] = useState(1);

    // Example data for rooms (replace with actual data or API call)
    const rooms = [
        {
            id: 1,
            name: 'Phòng Deluxe',
            type: 'Suite',
            price: 150,
            image: 'https://via.placeholder.com/300x200',
        },
        {
            id: 2,
            name: 'Phòng Standard',
            type: 'Standard',
            price: 100,
            image: 'https://via.placeholder.com/300x200',
        },
        {
            id: 3,
            name: 'Phòng Family',
            type: 'Family',
            price: 200,
            image: 'https://via.placeholder.com/300x200',
        },
    ];

    const handleSearch = () => {
        // Xử lý tìm kiếm khách sạn
        console.log('Searching hotels...');
    };

    return (
        <div css={styles}>
            <div className="search-container">
                <h1>Tìm kiếm khách sạn</h1>
                <div className="search-form">
                    <input
                        type="text"
                        placeholder="Địa điểm, tên khách sạn..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    <input
                        type="date"
                        value={checkInDate}
                        onChange={(e) => setCheckInDate(e.target.value)}
                    />
                    <input
                        type="date"
                        value={checkOutDate}
                        onChange={(e) => setCheckOutDate(e.target.value)}
                    />
                    <input
                        type="number"
                        placeholder="Số lượng khách"
                        value={numGuests}
                        onChange={(e) => setNumGuests(e.target.value)}
                    />
                    <button onClick={handleSearch}>Tìm kiếm</button>
                </div>
            </div>
            <div className="hotel-list">
                <h2>Danh sách khách sạn</h2>
                {rooms.length > 0 ? (
                    <div className="room-cards">
                        {rooms.map((room) => (
                            <RoomCard key={room.id} room={room} />
                        ))}
                    </div>
                ) : (
                    <p>Chưa có kết quả tìm kiếm</p>
                )}
            </div>
        </div>
    );
};

const styles = css`
    margin-top: 100px; /* Khoảng cách giữa MainContent và Navbar */
    padding: 20px; /* Để nội dung bên trong không bị sát vào viền */

    .search-container {
        background-color: #f2f2f2;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .search-form {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }

    input[type='text'],
    input[type='date'],
    input[type='number'] {
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 16px;
        flex: 1;
        min-width: 200px;
    }

    button {
        padding: 12px 24px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 4px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #0056b3;
    }

    .hotel-list {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .room-cards {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }
`;

export default MainContent;
