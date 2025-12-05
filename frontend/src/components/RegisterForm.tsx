import React, { useState } from 'react'
import axios from 'axios'
import Message from './Message'

const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000/api';

interface FormErrors {
  login?: string
  password?: string
}

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState({
    login: '',
    password: ''
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  const [errors, setErrors] = useState<FormErrors>({})

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}

    // Валидация логина
    if (formData.login.length < 3 || formData.login.length > 32) {
      newErrors.login = 'Логин должен быть от 3 до 32 символов'
    } else if (!/^[a-zA-Z0-9._-]+$/.test(formData.login)) {
      newErrors.login = 'Логин может содержать только латинские буквы, цифры и символы . _ -'
    }

    // Валидация пароля
    const password = formData.password
    if (password.length < 8) {
      newErrors.password = 'Пароль должен быть не менее 8 символов'
    } else {
      const hasUpperCase = /[A-Z]/.test(password)
      const hasLowerCase = /[a-z]/.test(password)
      const hasNumbers = /\d/.test(password)
      const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)

      const missingRequirements = []
      if (!hasUpperCase) missingRequirements.push('заглавную букву')
      if (!hasLowerCase) missingRequirements.push('строчную букву')
      if (!hasNumbers) missingRequirements.push('цифру')
      if (!hasSpecialChar) missingRequirements.push('специальный символ')

      if (missingRequirements.length > 0) {
        newErrors.password = `Пароль должен содержать хотя бы: ${missingRequirements.join(', ')}`
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setLoading(true)
    setMessage(null)

    try {
      const response = await axios.post(`${API_URL}/register`, formData)
      
      if (response.status === 200) {
        setMessage({ type: 'success', text: 'Пользователь успешно зарегистрирован!' })
        setFormData({ login: '', password: '' })
      }
    } catch (error: any) {
      console.error('Registration error:', error)
      
      if (error.response) {
        const { status, data } = error.response
        
        switch (status) {
          case 409:
            setMessage({ type: 'error', text: 'Пользователь с таким логином уже существует' })
            break
          case 422:
            if (data.detail) {
              const fieldErrors = data.detail.map((err: any) => 
                `${err.loc[1]}: ${err.msg}`
              ).join(', ')
              setMessage({ type: 'error', text: `Ошибка валидации: ${fieldErrors}` })
            } else {
              setMessage({ type: 'error', text: 'Ошибка валидации данных' })
            }
            break
          default:
            setMessage({ type: 'error', text: `Ошибка сервера: ${data.message || 'Неизвестная ошибка'}` })
        }
      } else if (error.request) {
        setMessage({ type: 'error', text: 'Не удалось подключиться к серверу' })
      } else {
        setMessage({ type: 'error', text: 'Ошибка при отправке запроса' })
      }
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Очищаем ошибку при изменении поля
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  return (
    <div className="register-container">
      <h1>Регистрация пользователя</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="login">Логин:</label>
          <input
            type="text"
            id="login"
            name="login"
            value={formData.login}
            onChange={handleChange}
            placeholder="Введите логин"
            required
          />
          {errors.login && <div className="error-text">{errors.login}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="password">Пароль:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Введите пароль"
            required
          />
          {errors.password && <div className="error-text">{errors.password}</div>}
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Регистрация...' : 'Зарегистрироваться'}
        </button>
      </form>

      {message && <Message type={message.type} message={message.text} />}

      <div className="password-rules">
        <h3>Требования к паролю:</h3>
        <ul>
          <li>Минимум 8 символов</li>
          <li>Минимум 1 заглавная буква (A-Z)</li>
          <li>Минимум 1 строчная буква (a-z)</li>
          <li>Минимум 1 цифра (0-9)</li>
          <li>Минимум 1 специальный символ (!@#$%^&* и т.д.)</li>
        </ul>
      </div>
    </div>
  )
}

export default RegisterForm
