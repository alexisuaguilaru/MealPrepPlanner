import streamlit as st

def Footer():
    st.divider()

    with st.container(horizontal=True,vertical_alignment='center',horizontal_alignment='center'):
        st.markdown(
            '[![](/app/static/School.png)](https://www.enesmorelia.unam.mx)',
            width = 100,
            text_alignment = 'left',
        )

        st.space('medium')

        st.markdown(
            '[**Alexis Aguilar**](https://github.com/alexisuaguilaru)',
            text_alignment = 'center',
        )

        st.space('medium')

        st.markdown(
            '[![](/app/static/Bachelors.png)](https://www.enesmorelia.unam.mx/licenciaturas/tecnologias-para-la-informacion-en-ciencias/)',
            width = 50,
            text_alignment = 'right',
        )

    with st.container(horizontal=True,vertical_alignment='center',horizontal_alignment='center'):
        if _AddLegalSelector('Aviso de Privacidad','privacy'):
            _ShowPrivacy()

        if _AddLegalSelector('Términos de Uso','terms_use'):
            _ShowTermsUso()

def _AddLegalSelector(LegalName,LegalKey):
    return st.button(
        f':small[{LegalName}]', 
        key = f'select_{LegalKey}',
    )

@st.dialog('Aviso de Privacidad Simplificado',width='large')
def _ShowPrivacy():
    st.markdown("""
    **Aplicación: Meal Prep Planner par Escuelas**
                
    1. *Responsable del Tratamiento:*
    El responsable del tratamiento de sus datos personales es Alexis Aguilar, con correo electrónico de contacto: alexis.uaguilaru@gmail.com.

    2. *Datos Personales que Recabamos:*
    Para prestar nuestros servicios de planificación de menús escolares, recabamos los siguientes datos personales:
        - Datos de identificación: Nombre completo, cargo (ej. nutricionista, administrador, padre de familia).
        - Datos de contacto: Correo electrónico, número telefónico.
        - Datos sensibles (si aplica): Información dietética, alergias alimentarias o restricciones médicas de los estudiantes (solo con consentimiento explícito y para fines estrictamente necesarios).
        - Datos de uso: Preferencias de menú, historial de selecciones y registros de acceso a la plataforma.
                
    3. *Finalidades del Tratamiento:*
    Sus datos personales serán utilizados para las siguientes finalidades necesarias para el servicio que solicitó:
        - Gestionar su cuenta de usuario y acceso a la plataforma.
        - Elaborar, personalizar y guardar planes de menús semanales.
        - Enviar notificaciones sobre cambios en los menús o actualizaciones de la app.
        - Generar reportes nutricionales agregados y anónimos para mejora del servicio.
                
    4. *Transferencia de Datos:*
    Sus datos no serán compartidos con terceros ajenos a esta relación, salvo:
    Proveedores de servicios tecnológicos (hosting, nube) que actúan como encargados del tratamiento bajo estrictos contratos de confidencialidad.
    Autoridades competentes, cuando sea requerido por ley.
    En caso de fusiones o adquisiciones empresariales, siempre garantizando la protección de sus datos.
                
    5. *Derechos ARCO y Limitación del Uso:*
    Usted tiene derecho a Acceder, Rectificar, Cancelar u Oponerse al tratamiento de sus datos personales (Derechos ARCO), así como a revocar el consentimiento otorgado.
    Para ejercer estos derechos, envíe una solicitud a [Correo Electrónico] indicando claramente qué derecho desea ejercer y adjuntando identificación oficial.
    Contaremos con un plazo máximo de [20 días hábiles] para responder su solicitud, conforme a la ley mexicana.
                
    6. *Seguridad de la Información:*
    Implementamos medidas de seguridad administrativas, técnicas y físicas (como encriptación de datos y accesos restringidos) para proteger sus datos personales contra daño, pérdida, alteración, destrucción o uso, acceso o tratamiento no autorizado.
                
    7. *Cambios al Aviso de Privacidad:*
    Nos reservamos el derecho de efectuar modificaciones al presente aviso de privacidad. Cualquier cambio será notificado a través de la aplicación o mediante correo electrónico. Le recomendamos revisar periódicamente este aviso.
                
    8. *Consentimiento (Para datos sensibles):*
    En caso de proporcionar información sobre alergias o condiciones de salud de menores de edad, declaro bajo protesta de decir verdad que soy el tutor legal o tengo la autorización expresa para compartir dicha información, entendiendo que es necesaria para la seguridad alimentaria del estudiante.
    """)

@st.dialog('Términos de Uso Simplificado',width='large')
def _ShowTermsUso():
    st.markdown("""
    **Aplicación: Meal Prep Planner par Escuelas**
                
    1. *Aceptación de los Términos:*
    Al acceder, registrarse o utilizar "Meal Prep Planner par Escuelas" (en adelante, "la Plataforma"), usted acepta quedar vinculado por estos Términos y Condiciones. Si no está de acuerdo con alguna parte de los mismos, le rogamos no utilice la Plataforma.
                
    2. *Descripción del Servicio:*
    La Plataforma es una herramienta digital diseñada para facilitar la planificación, gestión y visualización de menús semanales en entornos escolares. No somos un servicio de catering ni proveedores de alimentos; somos una herramienta de software para la organización logística y nutricional.
                
    3. *Registro y Seguridad de la Cuenta:*
    Usted es responsable de mantener la confidencialidad de sus credenciales de acceso (usuario y contraseña).
    Se compromete a notificar inmediatamente a Meal Planner cualquier uso no autorizado de su cuenta.
    Al registrarse, garantiza que la información proporcionada es veraz, actual y completa.
                
    4. *Propiedad Intelectual:*
    Todo el contenido presente en la Plataforma (código, diseño, logotipos, textos, gráficos) es propiedad exclusiva de Meal Planner o de sus licenciantes y está protegido por las leyes de propiedad intelectual de México y tratados internacionales. Queda prohibida su reproducción total o parcial sin autorización expresa.
                
    5. *Conducta del Usuario y Uso Aceptable:*
    Usted se compromete a NO utilizar la Plataforma para:
    Introducir datos falsos o engañosos sobre alergias o condiciones de salud de terceros.
    Violar leyes locales, estatales o federales aplicables.
    Intentar acceder a áreas restringidas del sistema o interferir con su funcionamiento técnico.
    Acosar, difamar o dañar a otros usuarios o personal escolar.
                
    6. *Limitación de Responsabilidad (Importante):*
    Precisión de la Información: La Plataforma ofrece herramientas de cálculo y sugerencias nutricionales basadas en bases de datos generales. Meal Planner no garantiza la exactitud absoluta de los valores nutricionales y no sustituye el consejo de un nutricionista certificado o médico profesional.
    Salud y Alergias: El usuario (escuela/padres) es el único responsable de verificar que los menús generados cumplan con las necesidades específicas de salud de los estudiantes. No nos hacemos responsables por reacciones alérgicas o problemas de salud derivados del uso incorrecto de la información planificada.
    Disponibilidad: No garantizamos que el servicio esté libre de errores o disponible ininterrumpidamente.
                
    7. *Privacidad y Protección de Datos:*
    El tratamiento de sus datos personales se rige por nuestro Aviso de Privacidad, el cual forma parte integral de estos términos. Al usar la Plataforma, usted consiente el tratamiento de sus datos conforme a dicho aviso, especialmente en lo referente a datos sensibles (salud/alergias) de menores de edad, bajo la supervisión del titular de la patria potestad.
                
    8. *Suspensión o Terminación del Servicio:*
    Nos reservamos el derecho de suspender o cancelar su acceso a la Plataforma, sin previo aviso, si incumple estos Términos y Condiciones o si su conducta afecta la seguridad o integridad del servicio.
                
    9. *Ley Aplicable y Jurisdicción:*
    Estos Términos se rigen por las leyes de los Estados Unidos Mexicanos. Cualquier controversia derivada del uso de la Plataforma será sometida a la jurisdicción de los tribunales competentes en la ciudad de [Ciudad, Estado], renunciando a cualquier otro fuero que pudiera corresponderles.
                
    10. *Modificaciones:*
    Podemos actualizar estos Términos periódicamente. Las modificaciones entrarán en vigor desde su publicación en la Plataforma. Le recomendamos revisar esta sección regularmente.
                
    *Contacto:*
    Para dudas legales o reportes de incumplimiento, contacte a: alexis.uaguilaru@gmail.com.
    """)