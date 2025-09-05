-- Создание базы данных
CREATE DATABASE marketplace_db;

-- Подключение к базе данных
\c marketplace_db;

-- Создание таблицы для параметров
CREATE TABLE IF NOT EXISTS marketplace_parameters (
    id SERIAL PRIMARY KEY,
    param_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    required BOOLEAN DEFAULT FALSE,
    values JSONB,
    category_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов
CREATE INDEX IF NOT EXISTS idx_marketplace_parameters_category 
ON marketplace_parameters(category_id);

CREATE INDEX IF NOT EXISTS idx_marketplace_parameters_param_id 
ON marketplace_parameters(param_id);

CREATE INDEX IF NOT EXISTS idx_marketplace_parameters_required 
ON marketplace_parameters(required);

-- Комментарии к таблице
COMMENT ON TABLE marketplace_parameters IS 'Параметры товаров маркетплейса';
COMMENT ON COLUMN marketplace_parameters.param_id IS 'ID параметра в API';
COMMENT ON COLUMN marketplace_parameters.name IS 'Название параметра';
COMMENT ON COLUMN marketplace_parameters.description IS 'Описание параметра';
COMMENT ON COLUMN marketplace_parameters.required IS 'Обязательность параметра';
COMMENT ON COLUMN marketplace_parameters.values IS 'Возможные значения (JSON)';
COMMENT ON COLUMN marketplace_parameters.category_id IS 'ID категории товаров';
