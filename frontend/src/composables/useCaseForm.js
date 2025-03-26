import { ref, computed } from 'vue'
import { isAuthenticated } from '@/utils/auth.js';

export default function useCaseForm() {
    const loading = ref(false)
    const successMessage = ref('')
    const errorMessage = ref('')
    
    const validateForm = (formData) => {
        const errors = []
        
        if (!formData.title.trim()) errors.push('Title is required')
        
        // check if email is empty or not a valid email
        if (formData.contact.trim() && !formData.contact.match(/^\S+@\S+\.\S+$/)) {
            errors.push('Valid email is required')
        }
        
        if (formData.technologies.length === 0) errors.push('At least one technology is required')
        if (!formData.shortDescription.trim()) errors.push('Short description is required')
        
        // Institution validation
        if (formData.institution_id === 'new') {
            if (!formData.new_institution.name) errors.push('Institution name is required')
            if (!formData.new_institution.country) errors.push('Country is required')
        } else if (!formData.institution_id) {
            errors.push('Institution is required')
        }
        
        return errors
    }

    const submitForm = async (formData) => {
        const validationErrors = validateForm(formData)
        console.log('formData:', formData)
        console.log('formData new institution:',formData.new_institution)
        if (validationErrors.length > 0) {
            errorMessage.value = validationErrors.join(', ')
            return false
        }

         // Format date to DD-MM-YYYY
        const projectInitiationDateFormatted = formData.projectInitiationDate
        ? formData.projectInitiationDate.split('-').reverse().join('-')
        : '';

        // Check authentication
        const token = localStorage.getItem('authToken')
        if (!isAuthenticated()) {
            errorMessage.value = 'You must be logged in to submit a case.'
            return false
        }
        console.log('token:', token)

        

        try {

            // 1. Create institution if new
            let institutionId = 0
            if (formData.institution_id === 'new') {
                const institutionResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/institutions/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: formData.new_institution.name,
                        country: formData.new_institution.country,
                        state: formData.new_institution.state,
                        city: formData.new_institution.city,
                        latitude: 0,
                        longitude: 0
                    })
                })
                
                if (!institutionResponse.ok) throw new Error('Institution creation failed')
                const institutionData = await institutionResponse.json()
                institutionId = institutionData.id
            } else {
                institutionId = formData.institution_id
            }

            // 2. Create AI technologies
            const aiTechIds = []
            for (const tech of formData.technologies) {
                let techData = null
                if (!tech.id) {
                    const techResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/ai-technologies/`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name: tech.name })
                    })
                    if (!techResponse.ok) throw new Error(`AI technology "${tech.name}" creation failed`)
                    techData = await techResponse.json()
                }else{
                    techData = tech
                }
                
                aiTechIds.push(techData.id)
            }


            // 3. Create use case
            const useCasePayload = {
                title: formData.title,
                short_description: formData.shortDescription,
                full_description: formData.fullDescription,
                institution_id: institutionId,
                ai_technologies: aiTechIds,
                contact: formData.contact,
                project_initiation_date: projectInitiationDateFormatted,
                url: formData.url,
                logo_filename: formData.logoFilename,
                status: 'pending'
            }
            
            console.log('useCasePayload:', useCasePayload)

            const useCaseResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/use-cases/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}` },
                body: JSON.stringify(useCasePayload)
            })

            if (!useCaseResponse.ok) {
                const errorData = await useCaseResponse.json()
                throw new Error(errorData.detail || `HTTP error ${useCaseResponse.status}`);
            }
            successMessage.value = 'Case submitted successfully!'
            return true
        } catch (error) {
            if (error.response) {
                const errorData = await error.response.json()
                errorMessage.value = errorData.detail || 'Submission failed'
            } else {
                errorMessage.value = error.message || 'Submission failed'
            }
            return false
        } finally {
            loading.value = false
        }
    }
            


    return {
        loading,
        successMessage,
        errorMessage,
        validateForm,
        submitForm
    }
}