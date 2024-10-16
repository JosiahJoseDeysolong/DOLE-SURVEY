module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {          
            textAlign: {
                'justify': 'justify',
              },  
            colors: {
                'navyBlue': '#193441',
                'navyLightBlue': '#3E606F',
                'navyLighterBlue': '#91AAB4',
                'navyLightestBlue': '#CBDBD7',
                'beige': '#FCFFF5',
        },     
            spacing: {
                '50': '12.5rem',
        },},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
